from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import tempfile
import shutil
import time
import uuid
import re
import numpy as np
import faiss
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from google import genai
from google.genai.errors import APIError
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Initialize FastAPI app
app = FastAPI(title="Optimized Gemini GraphRAG Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Configuration
def get_api_key():
    """Dynamically read the active Gemini API key from environment or local .env fallback"""
    key = os.getenv("GEMINI_API_KEY")
    if not key and os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("GEMINI_API_KEY="):
                        return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    return key or "REPLACE_WITH_YOUR_NEW_KEY"

def get_gemini_model():
    """Dynamically read the active Gemini model from environment or local .env fallback"""
    model = os.getenv("GEMINI_MODEL")
    if not model and os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("GEMINI_MODEL="):
                        return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    return model or "gemini-2.5-flash"
def handle_gemini_exception(e: Exception, model_name: str):
    """Categorize and raise clear, actionable HTTPExceptions based on Gemini client or upstream network errors."""
    err_msg = str(e)
    
    # 1. Socket/DNS / getaddrinfo resolution errors
    if "getaddrinfo" in err_msg or "socket.gaierror" in err_msg or "gaierror" in err_msg or "11001" in err_msg or "DNS" in err_msg or "connection" in err_msg.lower():
        raise HTTPException(
            status_code=503,
            detail="Network/DNS Error: Cannot resolve or reach Google Gemini API (generativelanguage.googleapis.com). Please verify your internet connection, active VPN, or system proxy configuration."
        )
        
    # 2. Permission Denied / Authorization Errors (401, 403)
    if "401" in err_msg or "403" in err_msg or "API key not valid" in err_msg.lower() or "permissiondenied" in err_msg.lower() or "unauthorized" in err_msg.lower() or "key" in err_msg.lower():
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key: The provided Gemini API Key is unauthorized, invalid, or scanner-revoked. Please generate a fresh, active API key from Google AI Studio."
        )
        
    # 3. Model Not Found / Unsupported Model (404)
    if "404" in err_msg or "not found" in err_msg.lower() or "notfound" in err_msg.lower() or "unsupported" in err_msg.lower():
        raise HTTPException(
            status_code=404,
            detail=f"Unsupported Model Name: The configured model '{model_name}' was not found or is unsupported by your API key. Please switch to a supported model like 'gemini-2.5-flash' or 'gemini-1.5-flash-latest'."
        )
        
    # 4. Quota Exceeded / Rate Limit (429)
    if "429" in err_msg or "resourceexhausted" in err_msg.lower() or "quota" in err_msg.lower() or "rate limit" in err_msg.lower():
        raise HTTPException(
            status_code=429,
            detail="Rate Limit / Quota Exceeded: Your Google Generative AI free-tier quota has been exhausted. Please wait 60 seconds or switch to a paid API key."
        )
        
    # Fallback default
    raise HTTPException(
        status_code=500,
        detail=f"Configuration/Initialization Error: The configured model '{model_name}' or API key returned an upstream error. Technical details: {err_msg}"
    )

def validate_gemini_configuration(api_key: Optional[str], model_name: str):
    """Startup or first-request validation step that checks configured model supports text generation"""
    if not api_key or api_key == "REPLACE_WITH_YOUR_NEW_KEY":
        raise HTTPException(
            status_code=400,
            detail="Configuration Error: Gemini API Key is missing or not configured. Please supply a valid key via the sidebar or environment."
        )
    
    try:
        client = genai.Client(api_key=api_key)
        # Dry-run validation call to verify model capability and key status
        client.models.generate_content(
            model=model_name,
            contents="Test validation query",
            config={"max_output_tokens": 1}
        )
    except Exception as e:
        handle_gemini_exception(e, model_name)

def generate_with_retry(client, model_name, prompt, retries=3, delay=5):
    """Helper function to automatically retry queries with exponential backoff on 429 rate limits"""
    for i in range(retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "ResourceExhausted" in err_msg or "quota" in err_msg.lower():
                if i < retries - 1:
                    # Exponential wait: 5s, 10s, 15s...
                    time.sleep(delay * (i + 1))
                    continue
            raise e

# Models
class QueryRequest(BaseModel):
    query: str
    collection_id: str
    api_key: Optional[str] = None
    model: Optional[str] = None

class QueryResponse(BaseModel):
    llm_answer: str
    rag_answer: str
    graphrag_answer: str
    processing_time: float
    rag_chunks_used: int
    graph_nodes_used: int
    collection_id: str
    debug_info: Dict[str, Any]

class UploadResponse(BaseModel):
    collection_id: str
    message: str
    documents_processed: int
    chunks_created: int
    entities_extracted: int
    relationships_created: int
    viz_data: Optional[Dict[str, Any]] = None

# Global store
collections: Dict[str, Dict[str, Any]] = {}

print("--- [START] INITIALIZING FLASH-LATEST PIPELINE ---")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("--- [READY] SYSTEM ONLINE ---")

def extract_keywords(text: str) -> List[str]:
    words = re.findall(r'\b[A-Z][a-zA-Z]{3,}\b|\b[A-Z]{2,}\b', text)
    return list(set(words))[:15]

@app.post("/upload", response_model=UploadResponse)
async def upload(collection_id: Optional[str] = None, api_key: Optional[str] = None, files: List[UploadFile] = File(...)):
    if not collection_id: collection_id = str(uuid.uuid4())
    if collection_id not in collections:
        collections[collection_id] = {
            "docs": [], "chunks": [], "graph_nodes": {}, "graph_edges": [],
            "embeddings": None, "faiss_index": None, "api_key": api_key
        }
    c = collections[collection_id]
    if api_key:
        c["api_key"] = api_key
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    all_texts = []
    
    for f in files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{f.filename}") as tmp:
            shutil.copyfileobj(f.file, tmp)
            path = tmp.name
        try:
            # 1. ROBUST EXTRACTION (PDF / TXT / DOCX with full table data retrieval)
            if f.filename.lower().endswith('.docx'):
                import docx
                doc = docx.Document(path)
                paragraphs = []
                # Extract paragraph texts
                for p in doc.paragraphs:
                    if p.text.strip(): paragraphs.append(p.text)
                # Extract text within tables (highly crucial for experiences, projects and resume matrices)
                for table in doc.tables:
                    for row in table.rows:
                        row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                        if row_cells:
                            paragraphs.append(" | ".join(list(dict.fromkeys(row_cells)))) # deduplicate cells per row
                text = "\n".join(paragraphs)
                
                chunks = splitter.split_text(text)
                for i, ct in enumerate(chunks):
                    cid = f"{f.filename}_p0_c{i}"
                    c["chunks"].append({"id": cid, "text": ct, "source": f.filename, "page": 0})
                    all_texts.append(ct)
                    kws = extract_keywords(ct)
                    for kw in kws:
                        if kw not in c["graph_nodes"]: c["graph_nodes"][kw] = {"id": kw}
                        c["graph_edges"].append({"source": kw, "target": cid})
            else:
                doc = fitz.open(path)
                for page_num, page in enumerate(doc):
                    text = page.get_text()
                    if not text.strip(): continue
                    chunks = splitter.split_text(text)
                    for i, ct in enumerate(chunks):
                        cid = f"{f.filename}_p{page_num}_c{i}"
                        c["chunks"].append({"id": cid, "text": ct, "source": f.filename, "page": page_num})
                        all_texts.append(ct)
                        kws = extract_keywords(ct)
                        for kw in kws:
                            if kw not in c["graph_nodes"]: c["graph_nodes"][kw] = {"id": kw}
                            c["graph_edges"].append({"source": kw, "target": cid})
                doc.close()
            c["docs"].append({"filename": f.filename})
        finally:
            if os.path.exists(path): os.unlink(path)
            
    if all_texts:
        embs = embedding_model.encode(all_texts)
        idx = faiss.IndexFlatL2(embs.shape[1])
        idx.add(embs.astype('float32'))
        c["faiss_index"] = idx

    # Generate Initial Visualization
    nodes = []
    edges = []
    added_ids = set()
    for doc in c["docs"]:
        if doc["filename"] not in added_ids:
            nodes.append({"id": doc["filename"], "label": doc["filename"], "group": "document"})
            added_ids.add(doc["filename"])
    for ch in c["chunks"][:20]:
        ch_id = ch["id"]
        nodes.append({
            "id": ch_id, 
            "label": f"Chunk {ch_id.split('_')[-1]}", 
            "group": "chunk",
            "title": f"<b>CHUNK CONTENT:</b><br>{ch['text'][:300]}..." 
        })
        edges.append({"from": ch["source"], "to": ch_id, "label": "HAS_CHUNK"})
        chunk_kws = extract_keywords(ch["text"])
        prev_kw = None
        for kw in chunk_kws[:4]:
            if kw not in added_ids:
                nodes.append({
                    "id": kw, 
                    "label": kw, 
                    "group": "entity",
                    "title": f"<b>ENTITY:</b> {kw}<br>Type: Technical Concept"
                })
                added_ids.add(kw)
            
            edges.append({"from": ch_id, "to": kw, "label": "MENTIONS", "width": 1})
            
            if prev_kw:
                edges.append({
                    "from": prev_kw, 
                    "to": kw, 
                    "label": "CO_OCCURS", 
                    "color": "#ffaa00",
                    "width": 2,
                    "dashes": True
                })
            prev_kw = kw

    return UploadResponse(
        collection_id=collection_id, message="Indexed",
        documents_processed=len(files), chunks_created=len(c["chunks"]),
        entities_extracted=len(c["graph_nodes"]), relationships_created=len(c["graph_edges"]),
        viz_data={"nodes": nodes, "edges": edges}
    )

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    if request.collection_id not in collections: raise HTTPException(status_code=404)
    start = time.time()
    c = collections[request.collection_id]
    
    if not c["faiss_index"] or len(c["chunks"]) == 0:
        raise HTTPException(status_code=400, detail="No indexed chunks available in this collection.")
    
    # 1. SEMANTIC VECTOR RETRIEVAL (6 chunks)
    _, I = c["faiss_index"].search(embedding_model.encode([request.query]).astype('float32'), 6)
    retrieved = [c["chunks"][idx] for idx in I[0] if idx != -1 and idx < len(c["chunks"])]
    context = "\n\n".join([f"[Source: {ch['source']}, Page: {ch['page']+1}] {ch['text']}" for ch in retrieved])
    
    # Configure API key and model dynamically on every query to pick up changes instantly
    session_key = c.get("api_key")
    active_key = request.api_key or session_key or get_api_key()
    active_model = request.model or get_gemini_model()
    
    # Startup/first-request validation step: checks configured model and key
    validate_gemini_configuration(active_key, active_model)
    
    # Instantiate supported Google Gen AI client path
    client = genai.Client(api_key=active_key)
    
    # 2. PIPELINE A: BASIC RAG SYNTHESIS
    basic_rag_prompt = f"""
    You are a standard Retrieval-Augmented Generation (RAG) Assistant.
    Provide a professional, direct answer to the user question using ONLY the provided text segments.
    
    CONTEXT SEGMENTS:
    {context}
    
    QUESTION:
    {request.query}
    
    INSTRUCTIONS:
    - Answer the question factual and grounded strictly in the context segments.
    - Explicitly cite the page and document source for your facts (e.g. "[Source: resume.docx, Page 1]").
    - If the context doesn't contain the answer, say "Based on the provided text, I could not find information regarding..."
    """
    
    # 3. PIPELINE B: ADVANCED GRAPHRAG PATH SYNTHESIS (NotebookLM Grade)
    query_kws = extract_keywords(request.query)
    graph_context_elements = []
    for kw in query_kws:
        connected_chunks = [e["target"] for e in c["graph_edges"] if e["source"].lower() == kw.lower()]
        connected_entities = [e["source"] for e in c["graph_edges"] if e["target"] in connected_chunks]
        if connected_chunks:
            graph_context_elements.append(
                f"- Concept '{kw}' is structurally linked across {len(connected_chunks)} document chunks. "
                f"Highly associated terms in the knowledge index: {', '.join(set(connected_entities[:6]))}."
            )
            
    graph_structural_context = "\n".join(graph_context_elements) if graph_context_elements else "- Focus: Direct Semantic Chunk Retrieval."
    
    graph_rag_prompt = f"""
    You are an Advanced GraphRAG Co-Pilot (NotebookLM-grade).
    You possess access to standard vector context AND traversed semantic relationship nodes from our Knowledge Graph.
    
    DOCUMENT VECTOR CONTEXT:
    {context}
    
    KNOWLEDGE GRAPH REASONING PATHS:
    {graph_structural_context}
    
    USER QUESTION:
    {request.query}
    
    INSTRUCTIONS:
    - Ground your response heavily in the provided text segments.
    - Provide a deep, highly structured, analytical, and professional answer.
    - Synthesize or explain the user's query with rich context, summarizing projects, credentials, or experience details.
    - Cite source pages using bracketed citations next to your assertions (e.g. "[Page 1]").
    - Gracefully bridge overlapping concepts using the structural associations from the Knowledge Graph paths.
    - Format with bold key terms and professional bullet points.
    """
    
    try:
        basic_rag_answer = generate_with_retry(client, active_model, basic_rag_prompt)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini API Basic RAG Synthesis Failed: {str(e)}"
        )
        
    try:
        graphrag_answer = generate_with_retry(client, active_model, graph_rag_prompt)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini API GraphRAG Synthesis Failed: {str(e)}"
        )
        
    # The primary answer displayed in chat bubbles is the top-tier GraphRAG answer!
    llm_answer = graphrag_answer
    
    # 4. DYNAMIC SUB-GRAPH VISUALIZATION DATA (JSON for vis-network)
    nodes = []
    edges = []
    added_ids = set()
    
    for doc in c["docs"]:
        doc_id = doc["filename"]
        if doc_id not in added_ids:
            nodes.append({"id": doc_id, "label": doc_id, "group": "document"})
            added_ids.add(doc_id)
            
    for ch in retrieved:
        ch_id = ch["id"]
        if ch_id not in added_ids:
            nodes.append({
                "id": ch_id, 
                "label": f"Chunk {ch_id.split('_')[-1]}", 
                "group": "chunk",
                "title": f"<b>CHUNK CONTENT:</b><br>{ch['text'][:300]}..."
            })
            added_ids.add(ch_id)
        edges.append({"from": ch["source"], "to": ch_id, "label": "HAS_CHUNK"})
        
        chunk_kws = extract_keywords(ch["text"])
        for kw in chunk_kws[:3]:
            if kw not in added_ids:
                nodes.append({
                    "id": kw, 
                    "label": kw, 
                    "group": "entity",
                    "title": f"<b>ENTITY:</b> {kw}<br>Type: Traversed Semantic Link"
                })
                added_ids.add(kw)
            edges.append({"from": ch_id, "to": kw, "label": "MENTIONS"})
            
    return QueryResponse(
        llm_answer=llm_answer,
        rag_answer=basic_rag_answer,
        graphrag_answer=f"### 🧠 Traversed Knowledge Path Synthesis\n\n{graphrag_answer}",
        processing_time=time.time() - start,
        rag_chunks_used=len(retrieved),
        graph_nodes_used=len(nodes),
        collection_id=request.collection_id,
        debug_info={"retrieved_pages": [ch["page"]+1 for ch in retrieved], "viz_data": {"nodes": nodes, "edges": edges}}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
