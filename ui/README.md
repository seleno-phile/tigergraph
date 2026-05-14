# GraphRAG Multi-Document Intelligence Assistant

A comparison system that demonstrates how GraphRAG outperforms traditional RAG in multi-hop reasoning and complex document analysis.

## 🎯 Core Goal

**Prove GraphRAG answers complex questions better than traditional RAG**

This is not just a chatbot - it's a measurable comparison system showing the superiority of graph-based reasoning.

## 🏗️ System Architecture

### Two-System Comparison

#### 1. Basic RAG (Baseline)
- Documents → chunked into smaller pieces
- Convert chunks into embeddings
- Store in vector database (FAISS / Chroma)
- Retrieve top relevant chunks
- Send to LLM → generate answer
- **Output:** surface-level answers (limited reasoning)

#### 2. GraphRAG (Main System ⭐)
- Documents → chunked
- Extract entities + relationships
- Build knowledge graph (TigerGraph)
- Query graph for connected context
- Send structured context to LLM
- **Output:** multi-hop reasoning answers

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Start Backend (FastAPI)
```bash
python backend.py
# Server runs on http://localhost:8000
```

### Start Frontend (Streamlit)
```bash
streamlit run app.py
# Opens in browser automatically
```

## 📊 How It Works

### Step 1: Document Upload
- Upload PDFs/text files
- Store raw content
- Automatic processing

### Step 2: RAG Pipeline
- Chunk documents
- Generate embeddings
- Store in vector DB
- Query → retrieve top chunks
- Send to LLM → answer

### Step 3: GraphRAG Pipeline
- Chunk documents
- Extract entities (AI, ML, etc.)
- Create relationships
- Store in TigerGraph
- Query graph → fetch connected nodes
- Send structured context to LLM

## 🕸️ Graph Design

### Vertices:
- **Document** - Source documents
- **Chunk** - Text segments
- **Entity** - Extracted concepts

### Edges:
- **HAS_CHUNK** - Document contains chunks
- **MENTIONS** - Chunk mentions entity
- **RELATED_TO** - Entity relationships

## 🎯 Demo Strategy

Use questions that require reasoning:
- *"How are AI and Graph Databases connected?"*
- *"Explain relationship between scalability and ML"*
- *"Which concepts appear across multiple documents?"*

These force GraphRAG to outperform RAG.

## 💻 Tech Stack

- **Backend:** FastAPI
- **Frontend:** Streamlit
- **LLM:** OpenAI / Gemini / Ollama
- **RAG:** FAISS / ChromaDB
- **Graph:** TigerGraph
- **Embeddings:** Sentence Transformers

## 🔧 API Endpoints

### POST `/upload`
Upload documents for processing
```json
{
  "files": ["document1.pdf", "document2.txt"]
}
```

### POST `/query`
Query both systems
```json
{
  "query": "How are AI and Graph Databases connected?"
}
```

Response:
```json
{
  "rag_answer": "Surface level response...",
  "graphrag_answer": "Multi-hop reasoning response...",
  "processing_time": 2.34,
  "rag_chunks_used": 5,
  "graph_nodes_used": 12
}
```

### GET `/status`
Get system status
```json
{
  "documents_count": 3,
  "chunks_count": 15,
  "entities_count": 8,
  "relationships_count": 12,
  "systems_ready": true
}
```

## 🎨 Frontend Features

### Document Upload
- Drag & drop interface
- Multiple file support (PDF/TXT)
- Real-time processing status

### Query Interface
- Single input field
- Side-by-side comparison display
- Processing indicators

### Comparison View
```
RAG Answer          | GraphRAG Answer
--------------------|------------------
Partial response    | Structured response
Weak reasoning      | Multi-hop reasoning
```

### System Status
- Documents processed count
- Real-time metrics
- Architecture explanation

## 🔄 Implementation Status

### ✅ Completed
- FastAPI backend with mock implementations
- Streamlit frontend with comparison UI
- Document upload functionality
- Side-by-side answer display
- System status monitoring

### 🚧 Mock Implementations (Replace with Real)
- RAG processing (use FAISS/ChromaDB)
- GraphRAG processing (use TigerGraph)
- Entity extraction (use NLP models)
- LLM integration (OpenAI/Gemini)

## 🛠️ Real Implementation Steps

### 1. RAG Pipeline
```python
# Replace mock_rag_processing with:
from sentence_transformers import SentenceTransformer
import faiss
import chromadb

# Chunk documents
# Generate embeddings
# Store in vector DB
# Retrieve and generate answers
```

### 2. GraphRAG Pipeline
```python
# Replace mock_graphrag_processing with:
import pyTigerGraph as tg

# Extract entities with spaCy/NLTK
# Create relationships
# Build TigerGraph schema
# Query with multi-hop traversal
```

### 3. LLM Integration
```python
# Add LLM calls:
import openai

# Send retrieved context to LLM
# Generate structured answers
```

## 📈 Expected Results

The system will demonstrate:

**RAG Limitations:**
- Surface-level retrieval
- Limited context understanding
- Single-hop reasoning
- May miss complex relationships

**GraphRAG Advantages:**
- Multi-hop reasoning capability
- Structured relationship understanding
- Cross-document connections
- Deeper contextual insights

## 🎯 Demo Questions

Try these to see the difference:

1. *"How are AI and Graph Databases connected?"*
2. *"Explain relationship between scalability and ML"*
3. *"Which concepts appear across multiple documents?"*
4. *"What are the key differences between RAG and GraphRAG?"*
5. *"How does graph-based reasoning improve document analysis?"*

## 🚀 Deployment

### Local Development
```bash
# Terminal 1 - Backend
python backend.py

# Terminal 2 - Frontend
streamlit run app.py
```

### Production
```bash
# Use proper ASGI server
uvicorn backend:app --host 0.0.0.0 --port 8000

# Deploy Streamlit app
streamlit run app.py --server.port 8501
```

## 📊 Performance Metrics

Track these to prove GraphRAG superiority:

- **Answer Quality:** Depth of reasoning
- **Context Coverage:** Cross-document connections
- **Relationship Discovery:** Multi-hop insights
- **Processing Time:** Efficiency comparison

## 🔒 Security Considerations

- Input validation for file uploads
- Rate limiting for API calls
- Secure LLM API keys
- CORS configuration for production

## 🤝 Contributing

1. Implement real RAG pipeline
2. Add GraphRAG with TigerGraph
3. Integrate actual LLM calls
4. Add comprehensive testing
5. Optimize performance

## 📝 License

MIT License - Academic and research use encouraged.

## 📞 Support

For questions about implementation or extending the system, check the code comments and API documentation.

---

**Version:** 1.0.0 (Mock Implementation)
**Goal:** Demonstrate GraphRAG superiority over traditional RAG
**Focus:** Clarity and measurable performance difference

### 3. Open in browser

Navigate to:
- `http://localhost:8000` (Python default)
- `http://localhost:3000` (if using port 3000)
- `http://localhost:8080` (if using http-server)

## File Structure

```
ui/
├── index.html          # Main HTML structure
├── styles.css          # Styling and animations
├── dashboard.js        # Dashboard functionality (upload, query, metrics)
├── graph.js            # Graph visualization engine
├── server.py           # Python development server (optional)
└── README.md           # This file
```

## How to Use

### Upload Documents
1. Click the upload box on the left sidebar
2. Select PDF or TXT files (max 500MB each)
3. Files are automatically indexed and processed

### Query the Network
1. Type your query in the input box at the bottom
2. Press Enter or click the lightning bolt icon
3. Results appear with analysis and insights

### View Supply Chain Graph
- The right panel shows an interactive network graph
- Hover over nodes to highlight connections
- Click nodes to select them
- Orange nodes indicate delays
- Green indicates available alternatives

## Components

### HTML (index.html)
- Main dashboard layout with three sections:
  - Left: Document upload and metrics
  - Center: Analysis and insights
  - Right: Interactive graph visualization

### CSS (styles.css)
- Cyberpunk/futuristic color scheme
- Cyan (#00d4ff), Orange (#ffb800), Green (#00ff88)
- Dark backgrounds with subtle animations
- Responsive grid layout

### JavaScript (dashboard.js)
- File upload handling with drag-and-drop
- Query execution and results display
- Metrics calculation
- Document indexing simulation

### JavaScript (graph.js)
- Force-directed graph layout algorithm
- Canvas-based visualization
- Interactive node/edge rendering
- Real-time animation loop
- Node status indicators

## API Integration (For Production)

To connect to a real GraphRAG backend, modify `executeQuery()` in `dashboard.js`:

```javascript
async executeQuery() {
    const query = this.queryInput.value.trim();
    if (!query) return;

    const response = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, documents: this.documents })
    });

    const result = await response.json();
    this.displayResult(result);
}
```

## Browser Compatibility

- Chrome/Edge: 90+
- Firefox: 88+
- Safari: 14+
- Requires HTML5 Canvas support

## Performance Notes

- Graph visualization optimizes for 50-100 nodes
- Supports up to 500MB file upload
- Queries process in ~1-2 seconds (demo mode)
- Smooth 60 FPS animations on modern hardware

## Keyboard Shortcuts

- `Enter` in query box: Execute query
- `ESC`: Clear selections (future feature)
- `?`: Show help (future feature)

## Troubleshooting

### Port Already in Use
```bash
# Try a different port
python -m http.server 9000
```

### CORS Issues
Use a local server instead of opening HTML directly. The dashboard requires HTTP protocol for proper functionality.

### Graph Not Displaying
- Check browser console for JavaScript errors
- Ensure canvas support is available
- Try a different browser

## Future Enhancements

- [ ] Backend GraphRAG integration
- [ ] Real database storage
- [ ] Advanced filtering options
- [ ] Export reports to PDF
- [ ] Collaborative features
- [ ] Mobile responsive design
- [ ] Dark/Light theme toggle
- [ ] Custom graph layout options

## License

MIT License - Feel free to use and modify

## Support

For issues or questions, please check the console for error messages and ensure all files are properly installed.

---

**Version**: 1.0.0  
**Last Updated**: 2026-05-13  
**Status**: Ready for Development
