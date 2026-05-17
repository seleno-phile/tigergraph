# GraphRAG Multi-Document Intelligence Assistant

A powerful comparison system that demonstrates how GraphRAG outperforms traditional RAG and standalone LLMs in multi-hop reasoning and complex document analysis.

## 🎯 Core Goal

**Prove GraphRAG answers complex questions better than traditional RAG and standard LLMs** using real document context and knowledge graph synthesis.

## 🏗️ System Architecture

### Three-System Comparison

#### 1. LLM Only (Baseline)
- No document access.
- **Output:** General answers based on pre-training data.

#### 2. Basic RAG (Baseline)
- Documents → Text Extraction → Keyword Retrieval.
- **Output:** Surface-level answers based on direct text matches.

#### 3. GraphRAG (Advanced ⭐)
- Documents → Entity/Relationship Extraction → Knowledge Graph Context.
- **Output:** Synthesized answers using multi-hop reasoning across your document corpus.

## 🚀 Key Features

- **Session Isolation**: Each user works with an isolated document collection.
- **Robust Parsing**: Support for PDF, TXT, and **DOCX** files with error quarantine.
- **Security**: Hardened against XSS by avoiding unsafe HTML rendering of user/document content.
- **Live Visualization**: Interactive knowledge graph that updates as you upload documents.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Backend (FastAPI)
```bash
python backend.py
# Server runs on http://localhost:8000
```

### 3. Start Frontend (Streamlit)
```bash
streamlit run app.py
# Application accessible at http://localhost:8501
```

## 📊 How to Use

1. **Upload Documents**: Use the sidebar to upload PDF, TXT, or DOCX files.
2. **Query**: Enter a complex question requiring reasoning across multiple documents.
3. **Compare**: View side-by-side results showing the difference between LLM-only, Basic RAG, and GraphRAG.

## 🔧 Component Ports
- **Backend API**: `8000`
- **Streamlit UI (Primary)**: `8501`
- **Static Dashboard (Visualization)**: `8080` (Run `python server.py` to start)

---
**Version:** 1.2.0
**Status:** Multi-tenancy and 3-Way Comparison Enabled
