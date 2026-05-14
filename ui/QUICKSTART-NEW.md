# GraphRAG Multi-Document Intelligence Assistant - Quick Start

## 🚀 Get Started in 2 Minutes

### **One-Click Launch (Windows):**
```
1. Double-click: run.bat
2. Wait for services to start
3. Browser opens automatically
4. Done! 🎉
```

### **Manual Launch:**
```bash
# Terminal 1 - Backend
pip install -r requirements.txt
python backend.py

# Terminal 2 - Frontend (new terminal)
streamlit run app.py
```

---

## 🎯 What This System Does

**Compares two AI approaches:**
- **Basic RAG** (Traditional) → Surface-level answers
- **GraphRAG** (Advanced) → Multi-hop reasoning

**Goal:** Prove GraphRAG answers complex questions better.

---

## 📋 Step-by-Step Usage

### 1. **Upload Documents**
- Click "Browse files" or drag & drop
- Upload PDFs or text files
- Click "🚀 Process Documents"
- Wait for processing confirmation

### 2. **Ask Complex Questions**
Try these questions that require reasoning:
- *"How are AI and Graph Databases connected?"*
- *"Explain relationship between scalability and ML"*
- *"Which concepts appear across multiple documents?"*

### 3. **Compare Results**
- **Left side:** Basic RAG (limited reasoning)
- **Right side:** GraphRAG (deep analysis)
- Notice how GraphRAG finds connections across documents

### 4. **Analyze Differences**
- RAG: Direct text matching
- GraphRAG: Relationship understanding

---

## 💻 System Architecture

```
User Query
    ↓
├── Basic RAG Pipeline
│   Documents → Chunks → Embeddings → Vector DB → LLM → Answer
│
└── GraphRAG Pipeline
    Documents → Entities → Knowledge Graph → Multi-hop → LLM → Answer
```

---

## 🎨 Interface Overview

### Left Sidebar
- **System Status:** Active systems count
- **Architecture:** How each system works
- **Demo Questions:** Click to try examples

### Main Area
- **Document Upload:** File selection and processing
- **Query Input:** Single question input
- **Comparison Display:** Side-by-side answers

### Status Indicators
- 🟡 Processing (yellow pulse)
- 🟢 Complete (green)
- 🔴 Error (red)

---

## 🔧 Troubleshooting

### **"Python not found"**
```bash
# Install Python from python.org
# Check "Add to PATH" during installation
```

### **"Module not found"**
```bash
pip install -r requirements.txt
```

### **Port already in use**
- Backend uses port 8000
- Frontend uses port 8501
- Change ports in code if needed

### **Browser doesn't open**
- Manually visit: http://localhost:8501
- Check firewall/antivirus

### **Upload fails**
- Check file size (reasonable limits)
- Ensure PDF/TXT format
- Try smaller files first

---

## 📊 Expected Behavior

### Upload Phase
- Files processed into chunks and entities
- Knowledge graph built automatically
- Both systems ready for queries

### Query Phase
- Both systems process simultaneously
- RAG gives direct answers
- GraphRAG shows relationships and connections

### Comparison
- RAG: "Found this information..."
- GraphRAG: "Through analysis of relationships..."

---

## 🎯 Demo Questions to Try

**Multi-hop Reasoning:**
- *"How do AI and knowledge graphs work together?"*
- *"What connects machine learning to scalability?"*

**Cross-document Analysis:**
- *"Which technologies appear in multiple contexts?"*
- *"How are different concepts related?"*

**Complex Relationships:**
- *"Explain the connection between AI and graph databases"*
- *"How does scalability affect machine learning?"*

---

## 📈 Understanding Results

### Basic RAG Characteristics
- Direct text retrieval
- Surface-level information
- Single concept answers
- Limited context awareness

### GraphRAG Advantages
- Relationship discovery
- Multi-document connections
- Deeper reasoning
- Structured insights

---

## 🚀 Advanced Usage

### Custom Documents
- Upload your own PDFs/text files
- Try domain-specific questions
- Compare performance on your data

### API Access
```python
import requests

# Query both systems
response = requests.post("http://localhost:8000/query",
    json={"query": "Your question here"})
```

### System Status
```python
# Check system health
status = requests.get("http://localhost:8000/status")
```

---

## 🔄 Current Implementation

**✅ Working Now:**
- FastAPI backend with mock processing
- Streamlit frontend with comparison UI
- Document upload and processing
- Side-by-side answer display
- Real-time status updates

**🚧 Mock Implementations:**
- RAG processing (replace with FAISS/ChromaDB)
- GraphRAG processing (replace with TigerGraph)
- Entity extraction (replace with NLP models)
- LLM integration (replace with OpenAI/Gemini)

---

## 📚 Next Steps

1. **Try the demo** with included questions
2. **Upload your documents** for testing
3. **Compare answers** from both systems
4. **Implement real pipelines** (see README.md)
5. **Customize for your domain**

---

## 💡 Pro Tips

- **Start with simple questions** to understand the difference
- **Use complex questions** to see GraphRAG shine
- **Upload related documents** for better comparisons
- **Try the same question multiple times** to see consistency

---

## 🎉 You're Ready!

The GraphRAG Multi-Document Intelligence Assistant is now running.

**Launch:** Double-click `run.bat`

**Demo:** Try the questions in the sidebar

**Compare:** Watch GraphRAG outperform traditional RAG

---

*Demonstrating the power of graph-based reasoning! 🧠*