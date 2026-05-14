import streamlit as st
import requests
import time
from typing import List, Dict, Any

# Configure page
st.set_page_config(
    page_title="GraphRAG Multi-Document Intelligence Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .comparison-container {
        display: flex;
        gap: 2rem;
        margin: 2rem 0;
    }
    .rag-column, .graphrag-column {
        flex: 1;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid;
        min-height: 400px;
    }
    .rag-column {
        border-color: #ff6b6b;
        background-color: rgba(255, 107, 107, 0.05);
    }
    .graphrag-column {
        border-color: #4ecdc4;
        background-color: rgba(78, 205, 196, 0.05);
    }
    .column-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
    .rag-header {
        color: #ff6b6b;
    }
    .graphrag-header {
        color: #4ecdc4;
    }
    .answer-box {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        min-height: 300px;
        white-space: pre-wrap;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
        margin: 2rem 0;
        text-align: center;
    }
    .query-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 2rem 0;
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-processing {
        background-color: #ffc107;
        animation: pulse 2s infinite;
    }
    .status-complete {
        background-color: #28a745;
    }
    .status-error {
        background-color: #dc3545;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        text-align: center;
        margin: 0.5rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Backend API configuration
API_BASE_URL = "http://localhost:8000"  # Adjust as needed

class GraphRAGAssistant:
    def __init__(self):
        self.documents = []
        self.current_query = ""
        self.rag_answer = ""
        self.graphrag_answer = ""
        self.processing_status = "idle"  # idle, processing, complete, error

    def upload_documents(self, files) -> Dict[str, Any]:
        """Upload documents to the backend"""
        try:
            files_data = []
            for file in files:
                files_data.append(("files", (file.name, file.read(), file.type)))

            response = requests.post(f"{API_BASE_URL}/upload", files=files_data)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def query_systems(self, query: str) -> Dict[str, Any]:
        """Query both RAG and GraphRAG systems"""
        try:
            response = requests.post(
                f"{API_BASE_URL}/query",
                json={"query": query}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def main():
    assistant = GraphRAGAssistant()

    # Main header
    st.markdown('<div class="main-header">🧠 GraphRAG Multi-Document Intelligence Assistant</div>', unsafe_allow_html=True)

    # Sidebar with system info
    with st.sidebar:
        st.header("📊 System Status")

        # Metrics cards
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">2</div>
                <div class="metric-label">Systems Active</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(assistant.documents)}</div>
                <div class="metric-label">Documents</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # System architecture info
        st.subheader("🏗️ Architecture")
        st.markdown("""
        **Basic RAG (Baseline):**
        - Documents → Chunks → Embeddings → Vector DB → LLM

        **GraphRAG (Advanced):**
        - Documents → Entities → Knowledge Graph → Multi-hop Reasoning → LLM
        """)

        st.markdown("---")

        # Demo questions
        st.subheader("💡 Demo Questions")
        demo_questions = [
            "How are AI and Graph Databases connected?",
            "Explain relationship between scalability and ML",
            "Which concepts appear across multiple documents?",
            "What are the key differences between RAG and GraphRAG?",
            "How does graph-based reasoning improve document analysis?"
        ]

        for q in demo_questions:
            if st.button(q, key=f"demo_{q}", help="Click to use this question"):
                st.session_state.query_input = q

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        # Document Upload Section
        st.subheader("📄 Document Upload")
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Upload PDFs or text files for analysis",
            type=["pdf", "txt"],
            accept_multiple_files=True,
            help="Select multiple files to build the knowledge base"
        )

        if uploaded_files:
            if st.button("🚀 Process Documents", type="primary"):
                with st.spinner("Processing documents..."):
                    result = assistant.upload_documents(uploaded_files)
                    if "error" not in result:
                        assistant.documents = uploaded_files
                        st.success(f"✅ Successfully processed {len(uploaded_files)} documents")
                    else:
                        st.error(f"❌ Error processing documents: {result['error']}")

        st.markdown('</div>', unsafe_allow_html=True)

        # Query Section
        st.subheader("❓ Query Intelligence")
        st.markdown('<div class="query-section">', unsafe_allow_html=True)

        query = st.text_input(
            "Enter your question:",
            value=st.session_state.get('query_input', ''),
            placeholder="Ask a complex question requiring multi-hop reasoning...",
            help="Try questions that need understanding relationships across documents"
        )

        col_a, col_b = st.columns([1, 4])
        with col_a:
            query_button = st.button("🔍 Analyze", type="primary", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Comparison Results
        st.subheader("⚖️ System Comparison")

        if query_button and query:
            assistant.processing_status = "processing"
            assistant.current_query = query

            # Show processing status
            status_col1, status_col2 = st.columns(2)
            with status_col1:
                st.markdown("""
                <div style="text-align: center; padding: 1rem;">
                    <span class="status-indicator status-processing"></span>
                    <strong>Basic RAG</strong><br>
                    <small>Processing chunks...</small>
                </div>
                """, unsafe_allow_html=True)

            with status_col2:
                st.markdown("""
                <div style="text-align: center; padding: 1rem;">
                    <span class="status-indicator status-processing"></span>
                    <strong>GraphRAG</strong><br>
                    <small>Analyzing relationships...</small>
                </div>
                """, unsafe_allow_html=True)

            # Process query
            with st.spinner("Analyzing with both systems..."):
                time.sleep(2)  # Simulate processing time
                result = assistant.query_systems(query)

                if "error" not in result:
                    assistant.rag_answer = result.get("rag_answer", "No answer generated")
                    assistant.graphrag_answer = result.get("graphrag_answer", "No answer generated")
                    assistant.processing_status = "complete"
                else:
                    assistant.processing_status = "error"
                    st.error(f"Error: {result['error']}")

            st.rerun()

        # Display results
        if assistant.processing_status == "complete":
            st.markdown("""
            <div class="comparison-container">
                <div class="rag-column">
                    <div class="column-header rag-header">🔍 Basic RAG (Baseline)</div>
                    <div class="answer-box">{}</div>
                </div>
                <div class="graphrag-column">
                    <div class="column-header graphrag-header">🧠 GraphRAG (Advanced)</div>
                    <div class="answer-box">{}</div>
                </div>
            </div>
            """.format(assistant.rag_answer, assistant.graphrag_answer), unsafe_allow_html=True)

            # Analysis section
            st.markdown("---")
            st.subheader("📈 Analysis")

            analysis_col1, analysis_col2 = st.columns(2)

            with analysis_col1:
                st.markdown("**Basic RAG Characteristics:**")
                st.markdown("- Surface-level retrieval")
                st.markdown("- Limited context understanding")
                st.markdown("- Single-hop reasoning")
                st.markdown("- May miss complex relationships")

            with analysis_col2:
                st.markdown("**GraphRAG Advantages:**")
                st.markdown("- Multi-hop reasoning capability")
                st.markdown("- Structured relationship understanding")
                st.markdown("- Cross-document connections")
                st.markdown("- Deeper contextual insights")

        elif assistant.processing_status == "processing":
            st.info("🔄 Processing your query with both systems...")

        else:
            # Default state - show system description
            st.markdown("""
            <div class="comparison-container">
                <div class="rag-column">
                    <div class="column-header rag-header">🔍 Basic RAG (Baseline)</div>
                    <div class="answer-box">
Basic RAG System:
• Documents → Chunks → Embeddings
• Vector similarity search
• Top-k retrieval
• Direct LLM generation

Provides surface-level answers with limited reasoning across document relationships.
                    </div>
                </div>
                <div class="graphrag-column">
                    <div class="column-header graphrag-header">🧠 GraphRAG (Advanced)</div>
                    <div class="answer-box">
GraphRAG System:
• Documents → Entity extraction → Knowledge Graph
• Graph traversal for context
• Multi-hop relationship discovery
• Structured context to LLM

Enables deep reasoning and understanding of complex relationships across documents.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 0.8rem;">
        <strong>GraphRAG Multi-Document Intelligence Assistant</strong><br>
        Demonstrating the power of graph-based reasoning over traditional RAG approaches
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
