// Dashboard functionality
class Dashboard {
    constructor() {
        this.uploadBox = document.querySelector('.upload-box');
        this.queryInput = document.querySelector('.query-input');
        this.queryBtn = document.querySelector('.query-btn');
        this.documents = [];
        this.setupEventListeners();
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
        input.accept = '.pdf,.txt';
        input.onchange = (e) => this.handleFileSelect(e);
        input.click();
    }

    handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        this.uploadBox.style.backgroundColor = 'rgba(0, 212, 255, 0.15)';
        this.uploadBox.style.borderColor = '#00ff88';
    }

    handleFileDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        this.uploadBox.style.backgroundColor = 'rgba(0, 212, 255, 0.05)';
        this.uploadBox.style.borderColor = '#00d4ff';
        
        const files = e.dataTransfer.files;
        for (let file of files) {
            this.addDocument(file);
        }
    }

    handleFileSelect(e) {
        const files = e.target.files;
        for (let file of files) {
            this.addDocument(file);
        }
    }

    addDocument(file) {
        // Check file size (max 500MB)
        if (file.size > 500 * 1024 * 1024) {
            alert('File size exceeds 500MB limit');
            return;
        }

        // Check file type
        if (!['application/pdf', 'text/plain'].includes(file.type)) {
            alert('Only PDF and TXT files are supported');
            return;
        }

        const document = {
            id: Date.now(),
            name: file.name,
            size: file.size,
            type: file.type,
            uploadDate: new Date(),
            progress: 0
        };

        this.documents.push(document);
        this.simulateFileProcessing(document);
        this.updateDocumentsList();
    }

    simulateFileProcessing(document) {
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 30;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
                document.indexed = true;
                this.updateDocumentsList();
            }
            document.progress = progress;
            this.updateDocumentsList();
        }, 300);
    }

    updateDocumentsList() {
        const documentsList = document.querySelector('.documents-list');
        if (!documentsList) return;

        documentsList.innerHTML = '';

        this.documents.forEach(doc => {
            const docElement = document.createElement('div');
            docElement.className = 'document-item' + (doc.indexed ? ' indexed' : '');
            
            const name = document.createElement('span');
            name.className = 'doc-name';
            name.textContent = doc.name;

            const status = document.createElement('span');
            if (doc.indexed) {
                status.className = 'doc-status indexed-tag';
                status.textContent = 'INDEXED';
            } else {
                status.className = 'doc-status';
                status.textContent = Math.round(doc.progress) + '%';
            }

            docElement.appendChild(name);
            docElement.appendChild(status);
            documentsList.appendChild(docElement);
        });

        // Update metrics
        this.updateMetrics();
    }

    updateMetrics() {
        const metrics = {
            'RECORDS RETRIEVED': Math.floor(1200 + this.documents.length * 400),
            'RELEVANCE SCORE': Math.floor(75 + this.documents.length * 3)
        };

        const metricElements = document.querySelectorAll('.metric');
        metricElements.forEach(metric => {
            const label = metric.querySelector('.metric-label').textContent;
            const value = metrics[label];
            if (value !== undefined) {
                metric.querySelector('.metric-value').textContent = value + (label.includes('SCORE') ? '%' : 'K');
            }
        });
    }

    executeQuery() {
        const query = this.queryInput.value.trim();
        if (!query) return;

        console.log('Executing query:', query);
        
        // Simulate query processing
        this.queryBtn.disabled = true;
        this.queryBtn.textContent = '⟳';
        this.queryBtn.style.animation = 'spin 1s linear infinite';

        // Add spin animation
        if (!document.querySelector('#spinStyle')) {
            const style = document.createElement('style');
            style.id = 'spinStyle';
            style.textContent = `
                @keyframes spin {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }
            `;
            document.head.appendChild(style);
        }

        // Simulate processing time
        setTimeout(() => {
            this.queryBtn.disabled = false;
            this.queryBtn.textContent = '⚡';
            this.queryBtn.style.animation = 'none';
            
            // Show result (in production, this would fetch from server)
            this.showQueryResult(query);
        }, 1500);
    }

    showQueryResult(query) {
        // Create a notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 30px;
            right: 30px;
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid #00ff88;
            border-radius: 4px;
            padding: 15px 20px;
            color: #00ff88;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            z-index: 1000;
            animation: slideIn 0.3s ease;
            max-width: 300px;
        `;

        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(350px); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);

        notification.innerHTML = `
            <strong>✓ Query Processed</strong><br>
            <small>"${query}"</small><br>
            <small style="opacity: 0.7;">Results returned in 1.2ms</small>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new Dashboard();
    
    // Initialize with sample metrics
    dashboard.updateMetrics();
});
