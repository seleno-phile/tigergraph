# 🚀 GraphRAG Assistant - Setup Guide

## Complete Installation & Running Guide

This guide helps you get the GraphRAG Intelligence Assistant running on your system.

---

## Step 1: Install Requirements
Ensure you have Python 3.8+ installed. Install the necessary packages:
```bash
pip install -r requirements.txt
```

## Step 2: Start the Backend
The backend handles document parsing, storage, and retrieval logic.
```bash
python backend.py
```
*Default Port: 8000*

## Step 3: Start the Streamlit Frontend (Primary UI)
This is the main interface for document analysis and comparison.
```bash
streamlit run app.py
```
*Default Port: 8501*

## Step 4: Access the Dashboard (Optional Visualization)
If you wish to view the static visualization dashboard:
```bash
python server.py
```
*Default Port: 8080*

---

## 🛠️ Troubleshooting

### Port Collisions
- **Backend (8000)**: If 8000 is busy, modify the port in `backend.py` and update `API_BASE_URL` in `app.py`.
- **Streamlit (8501)**: Streamlit will automatically try 8502, 8503, etc., if 8501 is busy.
- **Static Server (8080)**: Change the `PORT` variable in `server.py` if needed.

### Document Parsing Errors
- Ensure PDFs are not password-protected.
- Large files may take a few seconds to process during upload.

---
**Last Updated:** 2026-05-16
**Version:** 1.1.0
