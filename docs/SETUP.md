# 🚀 GraphRAG Assistant - Setup Guide

## Complete Installation & Running Guide

This guide helps you get the GraphRAG Intelligence Assistant running on your system with correct environment configurations and dependencies.

---

## Step 1: Install Requirements
Ensure you have Python 3.8+ installed. Install the necessary runtime packages:
```bash
pip install -r requirements.txt
```

## Step 2: Configure Environment Variables
Before running the application, configure your credentials. Create a `.env` file in the root directory:

```env
# Google Gemini API Credentials
GEMINI_API_KEY="AIzaSyYourActiveStudioAPIKeyHere"

# Gemini Model Routing (Optional, defaults to gemini-2.5-flash)
GEMINI_MODEL="gemini-2.5-flash"
```

*Note: You can also override these keys dynamically in the frontend Streamlit interface under **🔑 Client Configuration** without restarting services.*

## Step 3: Start the Backend
The backend handles document parsing, similarity embedding storage, and multi-hop graph retrieval logic.
```bash
python backend.py
```
*Default Port: 8000*

## Step 4: Start the Streamlit Frontend (Primary UI)
This is the main interface for document analysis, multi-tenant indexing, and 3-way comparative querying.
```bash
streamlit run app.py
```
*Default Port: 8501*

## Step 5: Access the Dashboard (Optional Visualization)
If you wish to view the static visualization dashboard:
```bash
python server.py
```
*Default Port: 8080*

---

## 🛠️ Troubleshooting

### Upstream Gemini Gateway 404 (Model Not Found)
* **Symptom:** Submitting queries causes an `HTTP 400` / `Initialization Error` indicating that a specific model was not found.
* **Cause:** The backend is trying to query a model that is either retired (like `gemini-1.5-flash` in older setups) or not supported by your Google AI Studio account.
* **Solution:** Set the `GEMINI_MODEL` environment variable in your `.env` file to a supported model (e.g., `gemini-2.5-flash` or `gemini-1.5-flash-latest`), or configure it dynamically in the Streamlit sidebar.

### Configuration / API Key Errors (HTTP 400)
* **Symptom:** Error loading or calling the API, returning "Configuration Error: Gemini API Key is missing or not configured".
* **Solution:** Create a `.env` file with `GEMINI_API_KEY="AIzaSy..."`, or input your key directly into the **"Gemini API Key"** password field in the Streamlit sidebar.

### Quota Exceeded (HTTP 429)
* **Symptom:** Upstream error indicating rate limits have been exceeded.
* **Solution:** The backend automatically retries queries using exponential backoff. If rate limits are consistently hit on a free-tier key, wait 60 seconds before submitting subsequent queries or switch to a paid project key.

### Port Collisions
- **Backend (8000)**: If 8000 is busy, modify the port in `backend.py` and update `API_BASE_URL` in `app.py`.
- **Streamlit (8501)**: Streamlit will automatically try 8502, 8503, etc., if 8501 is busy.
- **Static Server (8080)**: Change the `PORT` variable in `server.py` if needed.

### Document Parsing Errors
- Ensure PDFs are not password-protected.
- Large files may take a few seconds to process during upload.

---
**Last Updated:** 2026-05-17
**Version:** 2.0.0
