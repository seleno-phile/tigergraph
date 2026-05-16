// Dashboard functionality - Rewired for GraphRAG Backend
class Dashboard {
    constructor() {
        this.uploadBox = document.getElementById('uploadBox');
        this.queryInput = document.getElementById('queryInput');
        this.queryBtn = document.getElementById('queryBtn');
        this.collectionId = localStorage.getItem('graphrag_collection_id');
        this.documents = [];
        this.baseUrl = DashboardConfig.api.baseUrl;
        this.setupEventListeners();
        this.updateSystemStatus();
    }

    setupEventListeners() {
        if (this.uploadBox) {
            this.uploadBox.addEventListener('click', () => this.triggerFileUpload());
            this.uploadBox.addEventListener('dragover', (e) => this.handleDragOver(e));
            this.uploadBox.addEventListener('drop', (e) => this.handleFileDrop(e));
        }

        if (this.queryBtn) {
            this.queryBtn.addEventListener('click', () => this.executeQuery());
        }

        if (this.queryInput) {
            this.queryInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.executeQuery();
            });
        }
    }

    triggerFileUpload() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.pdf,.txt,.docx';
        input.multiple = true;
        input.onchange = (e) => this.handleFileSelect(e);
        input.click();
    }

    handleDragOver(e) {
        e.preventDefault();
        this.uploadBox.style.backgroundColor = 'rgba(0, 212, 255, 0.1)';
    }

    async handleFileDrop(e) {
        e.preventDefault();
        this.uploadBox.style.backgroundColor = '';
        const files = e.dataTransfer.files;
        await this.uploadFiles(files);
    }

    async handleFileSelect(e) {
        const files = e.target.files;
        await this.uploadFiles(files);
    }

    async uploadFiles(files) {
        const formData = new FormData();
        for (let file of files) {
            formData.append('files', file);
        }

        const url = new URL(`${this.baseUrl}${DashboardConfig.api.endpoints.upload}`);
        if (this.collectionId) url.searchParams.append('collection_id', this.collectionId);

        try {
            this.queryBtn.textContent = '...';
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            
            if (result.collection_id) {
                this.collectionId = result.collection_id;
                localStorage.setItem('graphrag_collection_id', this.collectionId);
            }
            
            this.updateSystemStatus();
            alert(result.message || 'Upload successful');
        } catch (err) {
            console.error('Upload failed:', err);
            alert('Upload failed. Check console for details.');
        } finally {
            this.queryBtn.textContent = '⚡';
        }
    }

    async updateSystemStatus() {
        if (!this.collectionId) return;

        try {
            const response = await fetch(`${this.baseUrl}/status/${this.collectionId}`);
            const data = await response.json();
            
            if (data.error) return;

            document.getElementById('metricChunks').textContent = data.chunks_count || '0';
            document.getElementById('metricNodes').textContent = data.entities_count || '0';
            
            const list = document.getElementById('documentsList');
            list.innerHTML = ''; // Safe because we populate with textContent below
            
            if (data.documents_count === 0) {
                list.textContent = 'No documents uploaded';
            } else {
                // In a real app, we'd fetch the doc names from status or a separate endpoint
                const info = document.createElement('div');
                info.className = 'document-item indexed';
                info.textContent = `${data.documents_count} Document(s) active in session`;
                list.appendChild(info);
            }

            // Update Graph if possible
            if (window.GraphVisualizer && typeof window.GraphVisualizer.updateGraph === 'function') {
                const graphRes = await fetch(`${this.baseUrl}/graph/${this.collectionId}`);
                const graphData = await graphRes.json();
                window.GraphVisualizer.updateGraph(graphData.nodes, graphData.edges);
            }
        } catch (err) {
            console.error('Status check failed:', err);
        }
    }

    async executeQuery() {
        const query = this.queryInput.value.trim();
        if (!query) return;
        if (!this.collectionId) {
            alert('Please upload documents first.');
            return;
        }

        this.queryBtn.disabled = true;
        this.queryBtn.classList.add('spinning');
        document.getElementById('currentQueryLabel').textContent = `> "${query}"`;

        try {
            const startTime = Date.now();
            const response = await fetch(`${this.baseUrl}${DashboardConfig.api.endpoints.query}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: query,
                    collection_id: this.collectionId
                })
            });
            const result = await response.json();
            const latency = Date.now() - startTime;

            if (!response.ok) {
                const errorMsg = result.detail || result.error || 'Unknown error';
                document.getElementById('llmOnlyText').textContent = `Error: ${errorMsg}`;
                document.getElementById('ragText').textContent = `Error: ${errorMsg}`;
                document.getElementById('graphRagText').textContent = `Error: ${errorMsg}`;
                
                if (response.status === 404) {
                    alert('Session expired or server restarted. Please re-upload documents.');
                    this.collectionId = null;
                    localStorage.removeItem('graphrag_collection_id');
                }
                return;
            }

            document.getElementById('systemStatus').textContent = `SYSTEM: ONLINE // LATENCY: ${latency}ms`;
            
            // Safe DOM assignment
            document.getElementById('llmOnlyText').textContent = result.llm_answer || 'No answer generated';
            document.getElementById('ragText').textContent = result.rag_answer || 'No answer generated';
            document.getElementById('graphRagText').textContent = result.graphrag_answer || 'No answer generated';

        } catch (err) {
            console.error('Query failed:', err);
            const msg = 'Error: Failed to connect to backend server. Make sure it is running on port 8000.';
            document.getElementById('llmOnlyText').textContent = msg;
            document.getElementById('ragText').textContent = msg;
            document.getElementById('graphRagText').textContent = msg;
        } finally {
            this.queryBtn.disabled = false;
            this.queryBtn.classList.remove('spinning');
        }
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new Dashboard();
});
