import streamlit as st
import requests
import time
from typing import List, Dict, Any

# Configure page
st.set_page_config(
    page_title="GraphRAG AI Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Chat Experience
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(0, 212, 255, 0.1);
    }
    .main-header {
        background: linear-gradient(90deg, #00d4ff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .answer-card {
        background-color: rgba(10, 14, 39, 0.7);
        border: 1px solid #00d4ff;
        border-radius: 10px;
        padding: 20px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Backend API configuration
API_BASE_URL = "http://localhost:8000"

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'collection_id' not in st.session_state:
    st.session_state.collection_id = None
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'debug_data' not in st.session_state:
    st.session_state.debug_data = {}

def upload_files(files, progress_bar):
    try:
        progress_bar.info("📡 Connecting to GraphRAG Backend...")
        files_data = [("files", (f.name, f.read(), f.type)) for f in files]
        
        params = {"collection_id": st.session_state.collection_id} if st.session_state.collection_id else {}
        
        response = requests.post(f"{API_BASE_URL}/upload", files=files_data, params=params)
        if response.status_code != 200: return {"error": f"Error: {response.text}"}
        
        result = response.json()
        st.session_state.collection_id = result["collection_id"]
        st.session_state.documents.extend([f.name for f in files])
        
        # Display Progress Metrics
        cols = st.columns(4)
        cols[0].metric("Files", result['documents_processed'])
        cols[1].metric("Chunks", result['chunks_created'])
        cols[2].metric("Entities", result['entities_extracted'])
        cols[3].metric("Edges", result['relationships_created'])
        
        return result
    except Exception as e:
        return {"error": str(e)}

def query_backend(query: str):
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"query": query, "collection_id": st.session_state.collection_id}
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Sidebar
with st.sidebar:
    st.markdown("# 🧠 <span class='main-header'>GraphRAG</span>", unsafe_allow_html=True)
    st.caption("Intelligence System v2.0")
    
    st.subheader("📄 Knowledge Base")
    uploaded_files = st.file_uploader("Index Documents", type=["pdf", "txt", "docx"], accept_multiple_files=True)
    
    if uploaded_files and st.button("🚀 Process Intelligence"):
        progress_area = st.sidebar.empty()
        progress_area.info("📡 Connecting to GraphRAG Backend...")
        
        res = upload_files(uploaded_files, progress_area)
        progress_area.empty()
        
        if "error" not in res:
            st.session_state.collection_id = res["collection_id"]
            st.session_state.debug_data["indexing"] = res
            st.session_state.global_graph = res.get("viz_data")
            st.sidebar.success("✅ Intelligence Base Ready!")
        else:
            st.sidebar.error(res["error"])

    st.markdown("---")
    if st.session_state.collection_id:
        st.info(f"Active Session: {st.session_state.collection_id[:8]}")
        if st.button("🗑️ Clear History"):
            st.session_state.messages = []
            st.rerun()
        if st.button("🔄 Reset All"):
            st.session_state.messages = []; st.session_state.collection_id = None; st.session_state.documents = []
            st.rerun()

    st.markdown("---")
    if st.checkbox("🔍 Debug Visualization", value=False):
        st.subheader("🛠️ Internal Metrics")
        st.json(st.session_state.debug_data)

# Main Chat Interface
st.title("💬 Intelligent Assistant")
st.markdown("Traversing multi-document context using hybrid vector-graph search.")

if 'global_graph' in st.session_state and st.session_state.global_graph:
    with st.expander("🌐 Global Knowledge Map (Click to Explore)", expanded=True):
        import json
        graph_json = json.dumps(st.session_state.global_graph)
        html_content = f"""
        <div style="position: relative;">
            <div id="globalnetwork" style="width: 100%; height: 600px; background-color: #1c1c1c; border-radius: 10px;"></div>
            <div id="detailpanel" style="position: absolute; top: 10px; right: 10px; width: 250px; max-height: 580px; 
                background: rgba(10, 14, 39, 0.9); border: 1px solid #00d4ff; border-radius: 8px; color: white; padding: 15px; 
                overflow-y: auto; display: none; z-index: 100; font-family: sans-serif; font-size: 13px;">
                <h4 style="margin-top: 0; color: #00d4ff;">Node Details</h4>
                <div id="detailcontent">Select a node to see details.</div>
            </div>
        </div>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <script type="text/javascript">
            var data = {graph_json};
            var container = document.getElementById('globalnetwork');
            var panel = document.getElementById('detailpanel');
            var content = document.getElementById('detailcontent');
            
            var options = {{
                nodes: {{ shape: 'dot', size: 15, font: {{ size: 12, color: '#ffffff' }}, borderWidth: 2, shadow: true }},
                edges: {{ width: 1, font: {{ size: 8, align: 'middle', color: '#aaaaaa' }}, color: {{ color: '#444444', highlight: '#00d4ff' }}, arrows: {{ to: {{ enabled: true, scaleFactor: 0.5 }} }} }},
                groups: {{
                    document: {{ color: {{ background: '#82caff', border: '#5dade2' }} }},
                    chunk: {{ color: {{ background: '#6a5acd', border: '#483d8b' }} }},
                    entity: {{ color: {{ background: '#00bfff', border: '#008b8b' }} }}
                }},
                physics: {{
                    forceAtlas2Based: {{ gravitationalConstant: -30, centralGravity: 0.01, springLength: 80, springConstant: 0.05 }},
                    maxVelocity: 50, solver: 'forceAtlas2Based', stabilization: {{ iterations: 100 }}
                }}
            }};
            var network = new vis.Network(container, data, options);
            
            network.on("click", function (params) {{
                if (params.nodes.length > 0) {{
                    var nodeId = params.nodes[0];
                    var nodeData = data.nodes.find(n => n.id === nodeId);
                    panel.style.display = 'block';
                    content.innerHTML = "<b>ID:</b> " + nodeData.id + "<br><br>" + (nodeData.title || "No extra details available.");
                }} else {{
                    panel.style.display = 'none';
                }}
            }});
        </script>
        """
        st.components.v1.html(html_content, height=620)
st.markdown("---")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            with st.expander("🛠️ Retrieval & Reasoning Paths"):
                tab1, tab2 = st.tabs(["🔍 Basic RAG", "🧠 GraphRAG Path"])
                with tab1: st.markdown(message.get("rag_answer", ""))
                with tab2: st.markdown(message.get("graphrag_answer", ""))

# Chat Input
if prompt := st.chat_input("Ask a complex question about your documents..."):
    if not st.session_state.collection_id:
        st.error("Please index your documents first!")
    else:
        # User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant Response
        with st.chat_message("assistant"):
            with st.spinner("🤖 Synthesizing multi-hop answer..."):
                result = query_backend(prompt)
                
                if "error" not in result:
                    st.session_state.debug_data["last_query"] = result.get("debug_info", {})
                    
                    # 1. Final Synthesized Answer (The Core)
                    final_answer = result.get("llm_answer", "")
                    st.markdown(final_answer)
                    
                    # 2. Detailed Insights
                    with st.expander("🛠️ Retrieval & Reasoning Paths"):
                        tab1, tab2, tab3 = st.tabs(["🔍 Basic RAG", "🧠 GraphRAG Path", "🌐 Knowledge Explorer"])
                        with tab1: st.markdown(result.get("rag_answer", ""))
                        with tab2: st.markdown(result.get("graphrag_answer", ""))
                        with tab3: 
                            if "viz_data" in result:
                                import json
                                graph_json = json.dumps(result["viz_data"])
                                html_content = f"""
                                <div id="mynetwork" style="width: 100%; height: 500px; background-color: #1c1c1c; border-radius: 10px;"></div>
                                <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
                                <script type="text/javascript">
                                    var data = {graph_json};
                                    var container = document.getElementById('mynetwork');
                                    var options = {{
                                        nodes: {{
                                            shape: 'dot',
                                            size: 15,
                                            font: {{ size: 12, color: '#ffffff' }},
                                            borderWidth: 2,
                                            shadow: true
                                        }},
                                        edges: {{
                                            width: 1,
                                            font: {{ size: 8, align: 'middle', color: '#aaaaaa' }},
                                            color: {{ color: '#444444', highlight: '#00d4ff' }},
                                            arrows: {{ to: {{ enabled: true, scaleFactor: 0.5 }} }}
                                        }},
                                        groups: {{
                                            document: {{ color: {{ background: '#82caff', border: '#5dade2' }} }},
                                            chunk: {{ color: {{ background: '#6a5acd', border: '#483d8b' }} }},
                                            entity: {{ color: {{ background: '#00bfff', border: '#008b8b' }} }}
                                        }},
                                        physics: {{
                                            forceAtlas2Based: {{ gravitationalConstant: -30, centralGravity: 0.01, springLength: 80, springConstant: 0.05 }},
                                            maxVelocity: 50, solver: 'forceAtlas2Based', stabilization: {{ iterations: 100 }}
                                        }}
                                    }};
                                    var network = new vis.Network(container, data, options);
                                </script>
                                """
                                st.components.v1.html(html_content, height=520)
                            else:
                                st.info("Graph visualization not available for this query.")
                    
                    # Save to Session
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": final_answer,
                        "rag_answer": result.get("rag_answer", ""),
                        "graphrag_answer": result.get("graphrag_answer", ""),
                        "viz_data": result.get("viz_data", None)
                    })
                else:
                    st.error(f"Backend Failure: {result['error']}")

# Footer
st.markdown("---")
st.caption("Hybrid RAG Synthesis Engine | Powered by Graph & Vector Embeddings")
