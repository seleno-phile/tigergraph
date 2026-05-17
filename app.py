import streamlit as st
import requests
import time
import base64
import os
from typing import List, Dict, Any

# Configure page
st.set_page_config(
    page_title="GraphRAG AI Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load base64 assets for premium styling
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

cat_base64 = get_base64_image("cyber_cat.png")
bg_base64 = get_base64_image("cyber_bg.png")

# Custom CSS for Premium Chat Experience with Background and Cats
css_style = f"""
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
    /* Global Styles & Background Grid */
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    .stHeader, h1, h2, h3, h4, h5, h6 {{
        font-family: 'Space Grotesk', sans-serif;
    }}
    
    /* Background Image setup */
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
    
    /* Glass container around main page */
    .main .block-container {{
        background: rgba(11, 15, 25, 0.7) !important;
        backdrop-filter: blur(15px) saturate(180%);
        -webkit-backdrop-filter: blur(15px) saturate(180%);
        border-radius: 24px !important;
        padding: 40px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4) !important;
        margin-top: 30px !important;
        margin-bottom: 30px !important;
    }}
    
    /* Dark Theme Sidebar Overrides */
    [data-testid="stSidebar"] {{
        background-color: rgba(11, 15, 25, 0.85) !important;
        backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }}
    
    /* Chat bubbles styling */
    .stChatMessage {{
        background: rgba(17, 25, 40, 0.55) !important;
        backdrop-filter: blur(10px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 16px !important;
        margin-bottom: 20px !important;
        padding: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25) !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }}
    .stChatMessage:hover {{
        border-color: rgba(0, 212, 255, 0.25) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 212, 255, 0.1) !important;
    }}
    
    /* Linear Glowing Header */
    .glow-title {{
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #00f0ff 0%, #7000ff 50%, #ff007b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        letter-spacing: -0.5px;
        text-shadow: 0 0 40px rgba(0, 240, 255, 0.2);
    }}
    
    .sidebar-header {{
        background: linear-gradient(90deg, #00d4ff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 1.8rem;
    }}

    /* Custom Streamlit Button Styling */
    div.stButton > button:first-child {{
        background: linear-gradient(135deg, #00d4ff 0%, #7000ff 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(112, 0, 255, 0.25) !important;
        width: 100% !important;
    }}
    div.stButton > button:first-child:hover {{
        background: linear-gradient(135deg, #00d4ff 0%, #8a2be2 100%) !important;
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.4) !important;
        transform: translateY(-1px) !important;
    }}
    div.stButton > button:first-child:active {{
        transform: translateY(1px) !important;
    }}
    
    /* Metric Cards */
    .metric-container {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin: 20px 0;
    }}
    .metric-card {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }}
    .metric-card:hover {{
        background: rgba(0, 212, 255, 0.04);
        border-color: rgba(0, 212, 255, 0.25);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.08);
        transform: translateY(-3px);
    }}
    .metric-value {{
        font-size: 32px;
        font-weight: 700;
        color: #00d4ff;
        font-family: 'Space Grotesk', sans-serif;
        margin-bottom: 6px;
        text-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
    }}
    .metric-label {{
        font-size: 11px;
        font-weight: 600;
        color: #8c9ba5;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }}

    /* Custom styled tabs */
    div.stTabs [data-baseweb="tab-list"] {{
        gap: 8px !important;
        background-color: rgba(0, 0, 0, 0.25) !important;
        padding: 6px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }}
    div.stTabs [data-baseweb="tab"] {{
        height: 40px !important;
        white-space: pre-wrap !important;
        background-color: transparent !important;
        border-radius: 8px !important;
        color: #8c9ba5 !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        border: none !important;
        padding: 0 16px !important;
    }}
    div.stTabs [data-baseweb="tab"]:hover {{
        color: #00d4ff !important;
        background-color: rgba(255, 255, 255, 0.03) !important;
    }}
    div.stTabs [aria-selected="true"] {{
        background-color: rgba(0, 212, 255, 0.12) !important;
        color: #00d4ff !important;
        font-weight: 600 !important;
    }}
    
    /* Custom styled expanders */
    div.stExpander {{
        background: rgba(17, 25, 40, 0.35) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15) !important;
        margin-top: 10px !important;
    }}
    div.stExpander > details {{
        border: none !important;
    }}
    div.stExpander summary {{
        font-weight: 600 !important;
        color: #00d4ff !important;
    }}
    
    /* Network Map container */
    .network-container {{
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
        margin: 15px 0 !important;
    }}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

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
        
        # Display Premium HTML Progress Metrics
        metrics_html = f"""
        <div class="metric-container">
            <div class="metric-card">
                <div class="metric-value">{result['documents_processed']}</div>
                <div class="metric-label">📄 Files</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{result['chunks_created']}</div>
                <div class="metric-label">🧩 Chunks</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{result['entities_extracted']}</div>
                <div class="metric-label">🧠 Entities</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{result['relationships_created']}</div>
                <div class="metric-label">⚡ Connections</div>
            </div>
        </div>
        """
        st.markdown(metrics_html, unsafe_allow_html=True)
        
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
    # ORACLE-GR CyberCat Mascot
    if cat_base64:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 25px; padding-top: 10px;">
            <div style="display: inline-block; border-radius: 50%; padding: 4px; background: linear-gradient(135deg, #00d4ff, #7000ff); box-shadow: 0 0 25px rgba(0, 212, 255, 0.45); transition: all 0.3s ease;">
                <img src="data:image/png;base64,{cat_base64}" style="width: 140px; height: 140px; border-radius: 50%; object-fit: cover; display: block;" />
            </div>
            <div style="margin-top: 14px; font-weight: 700; font-size: 1.25rem; color: #00d4ff; font-family: 'Space Grotesk', sans-serif; text-shadow: 0 0 10px rgba(0,212,255,0.3);">ORACLE-GR</div>
            <div style="font-size: 0.8rem; color: #8c9ba5; letter-spacing: 1px; text-transform: uppercase;">CyberCat GraphRAG Co-Pilot</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("# 🧠 <span class='sidebar-header'>GraphRAG</span>", unsafe_allow_html=True)
        
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
            if 'global_graph' in st.session_state:
                del st.session_state.global_graph
            st.rerun()

    st.markdown("---")
    if st.checkbox("🔍 Debug Visualization", value=False):
        st.subheader("🛠️ Internal Metrics")
        st.json(st.session_state.debug_data)

# Main Chat Interface Header
st.markdown("""
<div style="text-align: center; padding: 25px; background: rgba(11, 15, 25, 0.45); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); max-width: 900px; margin: 0 auto 30px auto;">
    <h1 class="glow-title" style="font-size: 2.8rem; margin-bottom: 10px;">💬 GraphRAG AI Oracle</h1>
    <p style="color: #8c9ba5; font-size: 1.1rem; font-weight: 300; line-height: 1.5; margin: 0;">
        Traversing multi-document intelligence bases using deep hybrid semantic-graph vector exploration.
    </p>
</div>
""", unsafe_allow_html=True)

if len(st.session_state.messages) == 0:
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.05); 
                border-radius: 16px; padding: 30px; text-align: center; margin: 20px auto; max-width: 900px; box-shadow: 0 10px 30px rgba(0,0,0,0.25);">
        <div style="font-size: 2.5rem; margin-bottom: 12px; filter: drop-shadow(0 0 10px rgba(0, 212, 255, 0.3));">🔮</div>
        <h3 style="color: #00d4ff; font-family: 'Space Grotesk', sans-serif; margin-top: 0; margin-bottom: 8px; font-weight: 600;">System Awaiting Document Ingestion</h3>
        <p style="color: #8c9ba5; font-size: 0.95rem; line-height: 1.6; margin: 0;">
            To begin, upload files in the left sidebar and click <b>🚀 Process Intelligence</b>. 
            Once completed, <b>ORACLE-GR</b> will construct a deep concepts-and-chunks connection graph and stand ready to answer your most complex queries.
        </p>
    </div>
    """, unsafe_allow_html=True)

if 'global_graph' in st.session_state and st.session_state.global_graph:
    with st.expander("🌐 Global Knowledge Map (Click to Explore)", expanded=True):
        import json
        graph_json = json.dumps(st.session_state.global_graph)
        html_content = f"""
        <div style="position: relative;" class="network-container">
            <div id="globalnetwork" style="width: 100%; height: 600px; background-color: #0b0f19;"></div>
            <div id="detailpanel" style="position: absolute; top: 20px; right: 20px; width: 280px; max-height: 560px; 
                background: rgba(11, 15, 25, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(0, 212, 255, 0.3); 
                border-radius: 12px; color: white; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                overflow-y: auto; display: none; z-index: 100; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px;">
                <h4 style="margin-top: 0; color: #00d4ff; font-family: 'Space Grotesk', sans-serif; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px;">🔍 Node Intelligence</h4>
                <div id="detailcontent" style="line-height: 1.6;">Select a node to inspect...</div>
            </div>
        </div>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <script type="text/javascript">
            var data = {graph_json};
            var container = document.getElementById('globalnetwork');
            var panel = document.getElementById('detailpanel');
            var content = document.getElementById('detailcontent');
            
            var options = {{
                nodes: {{
                    shape: 'dot',
                    font: {{ size: 13, color: '#e2e8f0', face: 'Plus Jakarta Sans' }},
                    borderWidth: 2,
                    shadow: {{ enabled: true, color: 'rgba(0,0,0,0.5)', size: 10, x: 0, y: 4 }}
                }},
                edges: {{
                    width: 1.5,
                    font: {{ size: 9, align: 'middle', color: '#8c9ba5', face: 'Plus Jakarta Sans' }},
                    color: {{ color: 'rgba(255, 255, 255, 0.15)', highlight: '#00d4ff', hover: 'rgba(0, 212, 255, 0.4)' }},
                    arrows: {{ to: {{ enabled: true, scaleFactor: 0.6 }} }},
                    smooth: {{ type: 'cubicBezier', roundness: 0.5 }}
                }},
                groups: {{
                    document: {{
                        color: {{ background: '#00d4ff', border: '#00b4d8', highlight: {{ background: '#00f0ff', border: '#00d4ff' }} }},
                        size: 25
                    }},
                    chunk: {{
                        color: {{ background: '#7000ff', border: '#5a00d6', highlight: {{ background: '#8f00ff', border: '#7000ff' }} }},
                        size: 18
                    }},
                    entity: {{
                        color: {{ background: '#ff007b', border: '#d60067', highlight: {{ background: '#ff3399', border: '#ff007b' }} }},
                        size: 12
                    }}
                }},
                physics: {{
                    solver: 'forceAtlas2Based',
                    forceAtlas2Based: {{
                        gravitationalConstant: -80,
                        centralGravity: 0.015,
                        springLength: 120,
                        springConstant: 0.08,
                        damping: 0.4
                    }},
                    stabilization: {{ iterations: 150 }}
                }},
                interaction: {{ hover: true }}
            }};
            var network = new vis.Network(container, data, options);
            
            network.on("click", function (params) {{
                if (params.nodes.length > 0) {{
                    var nodeId = params.nodes[0];
                    var nodeData = data.nodes.find(n => n.id === nodeId);
                    panel.style.display = 'block';
                    
                    var groupLabel = nodeData.group ? nodeData.group.toUpperCase() : "UNKNOWN";
                    var badgeColor = nodeData.group === 'document' ? '#00d4ff' : (nodeData.group === 'chunk' ? '#7000ff' : '#ff007b');
                    
                    var html = "<span style='display:inline-block; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; background:" + badgeColor + "; color:white; margin-bottom:12px;'>" + groupLabel + "</span><br>";
                    html += "<b style='color:#e2e8f0; font-size:14px;'>" + nodeId + "</b><br><br>";
                    
                    var details = nodeData.title || "No further descriptive metadata available.";
                    html += "<div style='color:#a0aec0; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); padding:10px; border-radius:6px; max-height:300px; overflow-y:auto;'>" + details + "</div>";
                    
                    content.innerHTML = html;
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
                viz_data = message.get("viz_data")
                if viz_data:
                    tab1, tab2, tab3 = st.tabs(["🔍 Basic RAG", "🧠 GraphRAG Path", "🌐 Knowledge Explorer"])
                else:
                    tab1, tab2 = st.tabs(["🔍 Basic RAG", "🧠 GraphRAG Path"])
                
                with tab1: st.markdown(message.get("rag_answer", ""))
                with tab2: st.markdown(message.get("graphrag_answer", ""))
                
                if viz_data:
                    with tab3:
                        import json
                        graph_json = json.dumps(viz_data)
                        msg_hash = abs(hash(message['content']))
                        html_content = f"""
                        <div style="position: relative;" class="network-container">
                            <div id="mynetwork-{msg_hash}" style="width: 100%; height: 500px; background-color: #0b0f19;"></div>
                            <div id="detailpanel-{msg_hash}" style="position: absolute; top: 15px; right: 15px; width: 230px; max-height: 460px; 
                                background: rgba(11, 15, 25, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(0, 212, 255, 0.3); 
                                border-radius: 10px; color: white; padding: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.5);
                                overflow-y: auto; display: none; z-index: 100; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px;">
                                <h5 style="margin-top: 0; color: #00d4ff; font-family: 'Space Grotesk', sans-serif; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 6px;">🔍 Concept Intelligence</h5>
                                <div id="detailcontent-{msg_hash}" style="line-height: 1.5;">Select a node to inspect...</div>
                            </div>
                        </div>
                        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
                        <script type="text/javascript">
                            var data = {graph_json};
                            var container = document.getElementById('mynetwork-{msg_hash}');
                            var panel = document.getElementById('detailpanel-{msg_hash}');
                            var content = document.getElementById('detailcontent-{msg_hash}');
                            
                            var options = {{
                                nodes: {{
                                    shape: 'dot',
                                    font: {{ size: 12, color: '#e2e8f0', face: 'Plus Jakarta Sans' }},
                                    borderWidth: 2,
                                    shadow: {{ enabled: true, color: 'rgba(0,0,0,0.4)', size: 8, x: 0, y: 3 }}
                                }},
                                edges: {{
                                    width: 1.5,
                                    font: {{ size: 8, align: 'middle', color: '#8c9ba5', face: 'Plus Jakarta Sans' }},
                                    color: {{ color: 'rgba(255, 255, 255, 0.15)', highlight: '#00d4ff', hover: 'rgba(0, 212, 255, 0.4)' }},
                                    arrows: {{ to: {{ enabled: true, scaleFactor: 0.6 }} }},
                                    smooth: {{ type: 'cubicBezier', roundness: 0.5 }}
                                }},
                                groups: {{
                                    document: {{ color: {{ background: '#00d4ff', border: '#00b4d8' }}, size: 22 }},
                                    chunk: {{ color: {{ background: '#7000ff', border: '#5a00d6' }}, size: 16 }},
                                    entity: {{ color: {{ background: '#ff007b', border: '#d60067' }}, size: 10 }}
                                }},
                                physics: {{
                                    solver: 'forceAtlas2Based',
                                    forceAtlas2Based: {{
                                        gravitationalConstant: -60,
                                        centralGravity: 0.02,
                                        springLength: 100,
                                        springConstant: 0.08,
                                        damping: 0.4
                                    }},
                                    stabilization: {{ iterations: 100 }}
                                }},
                                interaction: {{ hover: true }}
                            }};
                            var network = new vis.Network(container, data, options);
                            
                            network.on("click", function (params) {{
                                if (params.nodes.length > 0) {{
                                    var nodeId = params.nodes[0];
                                    var nodeData = data.nodes.find(n => n.id === nodeId);
                                    panel.style.display = 'block';
                                    
                                    var groupLabel = nodeData.group ? nodeData.group.toUpperCase() : "UNKNOWN";
                                    var badgeColor = nodeData.group === 'document' ? '#00d4ff' : (nodeData.group === 'chunk' ? '#7000ff' : '#ff007b');
                                    
                                    var html = "<span style='display:inline-block; padding: 1px 6px; border-radius: 3px; font-size: 9px; font-weight: bold; background:" + badgeColor + "; color:white; margin-bottom:8px;'>" + groupLabel + "</span><br>";
                                    html += "<b style='color:#e2e8f0; font-size:12px;'>" + nodeId + "</b><br><br>";
                                    
                                    var details = nodeData.title || "No details available.";
                                    html += "<div style='color:#a0aec0; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); padding:8px; border-radius:4px; max-height:220px; overflow-y:auto;'>" + details + "</div>";
                                    
                                    content.innerHTML = html;
                                }} else {{
                                    panel.style.display = 'none';
                                }}
                            }});
                        </script>
                        """
                        st.components.v1.html(html_content, height=520)

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
                        viz_data = result.get("viz_data")
                        if viz_data:
                            tab1, tab2, tab3 = st.tabs(["🔍 Basic RAG", "🧠 GraphRAG Path", "🌐 Knowledge Explorer"])
                        else:
                            tab1, tab2 = st.tabs(["🔍 Basic RAG", "🧠 GraphRAG Path"])
                            
                        with tab1: st.markdown(result.get("rag_answer", ""))
                        with tab2: st.markdown(result.get("graphrag_answer", ""))
                        
                        if viz_data:
                            with tab3:
                                import json
                                graph_json = json.dumps(viz_data)
                                msg_hash = abs(hash(final_answer))
                                html_content = f"""
                                <div style="position: relative;" class="network-container">
                                    <div id="mynetwork-{msg_hash}" style="width: 100%; height: 500px; background-color: #0b0f19;"></div>
                                    <div id="detailpanel-{msg_hash}" style="position: absolute; top: 15px; right: 15px; width: 230px; max-height: 460px; 
                                        background: rgba(11, 15, 25, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(0, 212, 255, 0.3); 
                                        border-radius: 10px; color: white; padding: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.5);
                                        overflow-y: auto; display: none; z-index: 100; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px;">
                                        <h5 style="margin-top: 0; color: #00d4ff; font-family: 'Space Grotesk', sans-serif; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 6px;">🔍 Concept Intelligence</h5>
                                        <div id="detailcontent-{msg_hash}" style="line-height: 1.5;">Select a node to inspect...</div>
                                    </div>
                                </div>
                                <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
                                <script type="text/javascript">
                                    var data = {graph_json};
                                    var container = document.getElementById('mynetwork-{msg_hash}');
                                    var panel = document.getElementById('detailpanel-{msg_hash}');
                                    var content = document.getElementById('detailcontent-{msg_hash}');
                                    
                                    var options = {{
                                        nodes: {{
                                            shape: 'dot',
                                            font: {{ size: 12, color: '#e2e8f0', face: 'Plus Jakarta Sans' }},
                                            borderWidth: 2,
                                            shadow: {{ enabled: true, color: 'rgba(0,0,0,0.4)', size: 8, x: 0, y: 3 }}
                                        }},
                                        edges: {{
                                            width: 1.5,
                                            font: {{ size: 8, align: 'middle', color: '#8c9ba5', face: 'Plus Jakarta Sans' }},
                                            color: {{ color: 'rgba(255, 255, 255, 0.15)', highlight: '#00d4ff', hover: 'rgba(0, 212, 255, 0.4)' }},
                                            arrows: {{ to: {{ enabled: true, scaleFactor: 0.6 }} }},
                                            smooth: {{ type: 'cubicBezier', roundness: 0.5 }}
                                        }},
                                        groups: {{
                                            document: {{ color: {{ background: '#00d4ff', border: '#00b4d8' }}, size: 22 }},
                                            chunk: {{ color: {{ background: '#7000ff', border: '#5a00d6' }}, size: 16 }},
                                            entity: {{ color: {{ background: '#ff007b', border: '#d60067' }}, size: 10 }}
                                        }},
                                        physics: {{
                                            solver: 'forceAtlas2Based',
                                            forceAtlas2Based: {{
                                                gravitationalConstant: -60,
                                                centralGravity: 0.02,
                                                springLength: 100,
                                                springConstant: 0.08,
                                                damping: 0.4
                                            }},
                                            stabilization: {{ iterations: 100 }}
                                        }},
                                        interaction: {{ hover: true }}
                                    }};
                                    var network = new vis.Network(container, data, options);
                                    
                                    network.on("click", function (params) {{
                                        if (params.nodes.length > 0) {{
                                            var nodeId = params.nodes[0];
                                            var nodeData = data.nodes.find(n => n.id === nodeId);
                                            panel.style.display = 'block';
                                            
                                            var groupLabel = nodeData.group ? nodeData.group.toUpperCase() : "UNKNOWN";
                                            var badgeColor = nodeData.group === 'document' ? '#00d4ff' : (nodeData.group === 'chunk' ? '#7000ff' : '#ff007b');
                                            
                                            var html = "<span style='display:inline-block; padding: 1px 6px; border-radius: 3px; font-size: 9px; font-weight: bold; background:" + badgeColor + "; color:white; margin-bottom:8px;'>" + groupLabel + "</span><br>";
                                            html += "<b style='color:#e2e8f0; font-size:12px;'>" + nodeId + "</b><br><br>";
                                            
                                            var details = nodeData.title || "No details available.";
                                            html += "<div style='color:#a0aec0; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); padding:8px; border-radius:4px; max-height:220px; overflow-y:auto;'>" + details + "</div>";
                                            
                                            content.innerHTML = html;
                                        }} else {{
                                            panel.style.display = 'none';
                                        }}
                                    }});
                                </script>
                                """
                                st.components.v1.html(html_content, height=520)
                    
                    # Save to Session
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": final_answer,
                        "rag_answer": result.get("rag_answer", ""),
                        "graphrag_answer": result.get("graphrag_answer", ""),
                        "viz_data": viz_data
                    })
                else:
                    st.error(f"Backend Failure: {result['error']}")

# Footer
st.markdown("---")
st.caption("Hybrid RAG Synthesis Engine | Powered by Graph & Vector Embeddings")

