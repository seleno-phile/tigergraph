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
import google.generativeai as genai
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
GEMINI_API_KEY = "AIzaSyCr30OAno1BNSRJYxUN5NWG7jUTk0LED3o"
genai.configure(api_key=GEMINI_API_KEY)

# THE ONLY WORKING MODEL FOR THIS KEY BASED ON LIVE TESTING
PRIMARY_MODEL = "models/gemini-flash-latest"

# Models
class QueryRequest(BaseModel):
    query: str
    collection_id: str

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
async def upload(collection_id: Optional[str] = None, files: List[UploadFile] = File(...)):
    if not collection_id: collection_id = str(uuid.uuid4())
    if collection_id not in collections:
        collections[collection_id] = {
            "docs": [], "chunks": [], "graph_nodes": {}, "graph_edges": [],
            "embeddings": None, "faiss_index": None
        }
    c = collections[collection_id]
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
    
    model = genai.GenerativeModel(PRIMARY_MODEL)
    
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
        rag_resp = model.generate_content(basic_rag_prompt)
        basic_rag_answer = rag_resp.text
    except Exception as e:
        basic_rag_answer = f"⚠️ Basic RAG Error: {str(e)}"
        
    try:
        grag_resp = model.generate_content(graph_rag_prompt)
        graphrag_answer = grag_resp.text
    except Exception as e:
        graphrag_answer = f"⚠️ GraphRAG Error: {str(e)}"
        
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
