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

## 🔑 Configuration & Environment Variables

Create a `.env` file in the root directory to store your runtime credentials and configuration:

```env
# Google Gemini API Credentials
GEMINI_API_KEY="AIzaSyYourActiveStudioAPIKeyHere"

# Gemini Model Routing (Optional, defaults to gemini-2.5-flash)
GEMINI_MODEL="gemini-2.5-flash"
```

You can also override these keys dynamically in the Streamlit frontend sidebar expander under **"🔑 Client Configuration"** without restarting the backend!

## 🛠️ Troubleshooting

### 1. ⚠️ Upstream Gemini Gateway 404 (Model Not Found)
* **Cause:** The backend is trying to query a model that is either retired (like `gemini-1.5-flash` in older setups) or not supported by your Google AI Studio account.
* **Solution:** Ensure `GEMINI_MODEL` is configured to a valid, modern text-generation model like `gemini-2.5-flash` or `gemini-1.5-flash-latest`. You can adjust this on-the-fly in the sidebar configuration drawer.

### 2. ⚠️ Quota Exceeded (HTTP 429)
* **Cause:** Exceeding the rate limits of the Gemini API Free Tier.
* **Solution:** The backend automatically retries queries using exponential backoff. If failures persist, wait 60 seconds before submitting the query again or switch to a paid project key.

### 3. ⚠️ Configuration Error (HTTP 400)
* **Cause:** Missing `GEMINI_API_KEY` or invalid key input.
* **Solution:** Paste an active, valid key in the sidebar under "Gemini API Key" or save it directly into your local `.env` file in quotes.

## 🔧 Component Ports
- **Backend API**: `8000`
- **Streamlit UI (Primary)**: `8501`
- **Static Dashboard (Visualization)**: `8080` (Run `python server.py` to start)

---
**Version:** 2.0.0
**Status:** google-genai Compliant & Multi-Tenant Comparison Active
