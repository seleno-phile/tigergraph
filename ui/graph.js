// Supply Chain Graph Visualization
class SupplyChainGraph {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.nodes = [];
        this.edges = [];
        this.selectedNode = null;
        this.animationFrame = 0;
        this.time = 0;
        this.setupCanvas();
        this.initializeGraph();
        this.setupEventListeners();
        this.animate();
    }

    setupCanvas() {
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
        window.addEventListener('resize', () => this.resizeCanvas());
    }

    resizeCanvas() {
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
    }

    initializeGraph() {
        // Node positions - arranged in a network topology
        this.nodes = [
            { id: 'nexacorp', label: 'NexaCorp', type: 'supplier', x: 100, y: 150, color: '#ffb800', status: 'stable' },
            { id: 'vertexenergy', label: 'Vertex Energy', type: 'supplier', x: 100, y: 350, color: '#ffb800', status: 'delayed' },
            { id: 'taiwanfacility', label: 'Taiwan Facility', type: 'facility', x: 250, y: 250, color: '#00d4ff', status: 'stable' },
            { id: 'altpowerinc', label: 'Alt-Power Inc', type: 'supplier', x: 100, y: 500, color: '#00ff88', status: 'available' },
            { id: 'europeandistribution', label: 'European Distribution', type: 'distribution', x: 400, y: 250, color: '#9d9dff', status: 'blocked' },
            { id: 'assemblyph3', label: 'Assembly Ph.3', type: 'facility', x: 250, y: 100, color: '#00d4ff', status: 'delayed' },
        ];

        // Edge connections
        this.edges = [
            { from: 'nexacorp', to: 'taiwanfacility', label: 'Microprocessors', strength: 0.8 },
            { from: 'vertexenergy', to: 'taiwanfacility', label: 'Lithium Cells', strength: 0.9 },
            { from: 'taiwanfacility', to: 'assemblyph3', label: 'Assembly', strength: 0.85 },
            { from: 'assemblyph3', to: 'europeandistribution', label: 'Distribution', strength: 0.6 },
            { from: 'altpowerinc', to: 'taiwanfacility', label: 'Alt Supply', strength: 0.5 },
        ];

        // Apply force-directed layout
        this.applyForceDirectedLayout();
    }

    applyForceDirectedLayout() {
        const iterations = 50;
        const k = 150; // Optimal distance
        const c = 0.1; // Cooling factor

        for (let iter = 0; iter < iterations; iter++) {
            // Reset forces
            this.nodes.forEach(node => {
                node.vx = 0;
                node.vy = 0;
            });

            // Repulsive forces between all nodes
            for (let i = 0; i < this.nodes.length; i++) {
                for (let j = i + 1; j < this.nodes.length; j++) {
                    const dx = this.nodes[j].x - this.nodes[i].x;
                    const dy = this.nodes[j].y - this.nodes[i].y;
                    const distance = Math.sqrt(dx * dx + dy * dy) || 1;
                    const force = (k * k) / (distance * distance);

                    this.nodes[i].vx -= (force * dx) / distance;
                    this.nodes[i].vy -= (force * dy) / distance;
                    this.nodes[j].vx += (force * dx) / distance;
                    this.nodes[j].vy += (force * dy) / distance;
                }
            }

            // Attractive forces along edges
            this.edges.forEach(edge => {
                const from = this.nodes.find(n => n.id === edge.from);
                const to = this.nodes.find(n => n.id === edge.to);
                if (from && to) {
                    const dx = to.x - from.x;
                    const dy = to.y - from.y;
                    const distance = Math.sqrt(dx * dx + dy * dy) || 1;
                    const force = (distance - k) * c;

                    from.vx += (force * dx) / distance;
                    from.vy += (force * dy) / distance;
                    to.vx -= (force * dx) / distance;
                    to.vy -= (force * dy) / distance;
                }
            });

            // Update positions with boundary constraints
            this.nodes.forEach(node => {
                node.x += node.vx * 0.5;
                node.y += node.vy * 0.5;

                // Keep within bounds
                node.x = Math.max(30, Math.min(this.canvas.width - 30, node.x));
                node.y = Math.max(30, Math.min(this.canvas.height - 30, node.y));
            });
        }
    }

    setupEventListeners() {
        this.canvas.addEventListener('click', (e) => this.handleCanvasClick(e));
        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
    }

    handleCanvasClick(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        this.nodes.forEach(node => {
            const distance = Math.sqrt((node.x - x) ** 2 + (node.y - y) ** 2);
            if (distance < 30) {
                this.selectedNode = this.selectedNode === node.id ? null : node.id;
            }
        });
    }

    handleMouseMove(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        this.nodes.forEach(node => {
            const distance = Math.sqrt((node.x - x) ** 2 + (node.y - y) ** 2);
            node.hover = distance < 30;
        });
    }

    drawEdges() {
        this.ctx.strokeStyle = 'rgba(0, 212, 255, 0.3)';
        this.ctx.lineWidth = 1;

        this.edges.forEach(edge => {
            const from = this.nodes.find(n => n.id === edge.from);
            const to = this.nodes.find(n => n.id === edge.to);

            if (from && to) {
                // Draw edge
                this.ctx.beginPath();
                this.ctx.moveTo(from.x, from.y);
                this.ctx.lineTo(to.x, to.y);

                // Color based on status
                if (from.status === 'delayed' || to.status === 'delayed') {
                    this.ctx.strokeStyle = 'rgba(255, 184, 0, 0.4)';
                    this.ctx.lineWidth = 2;
                } else if (from.status === 'blocked' || to.status === 'blocked') {
                    this.ctx.strokeStyle = 'rgba(255, 68, 68, 0.3)';
                    this.ctx.lineWidth = 1.5;
                } else {
                    this.ctx.strokeStyle = 'rgba(0, 212, 255, 0.3)';
                    this.ctx.lineWidth = 1;
                }

                this.ctx.stroke();

                // Draw edge label
                const midX = (from.x + to.x) / 2;
                const midY = (from.y + to.y) / 2;
                this.ctx.fillStyle = 'rgba(0, 212, 255, 0.6)';
                this.ctx.font = '10px "Courier New"';
                this.ctx.textAlign = 'center';
                this.ctx.fillText(edge.label, midX, midY - 8);
            }
        });
    }

    drawNodes() {
        this.nodes.forEach(node => {
            const radius = node.hover || node.id === this.selectedNode ? 20 : 15;

            // Draw node circle
            this.ctx.beginPath();
            this.ctx.arc(node.x, node.y, radius, 0, Math.PI * 2);
            this.ctx.fillStyle = node.color;
            this.ctx.fill();

            // Draw border
            this.ctx.strokeStyle = node.id === this.selectedNode ? '#00ff88' : node.color;
            this.ctx.lineWidth = node.id === this.selectedNode ? 3 : 2;
            this.ctx.stroke();

            // Add glow effect for delayed/blocked nodes
            if (node.status === 'delayed') {
                this.ctx.shadowColor = 'rgba(255, 184, 0, 0.6)';
                this.ctx.shadowBlur = 15;
                this.ctx.strokeStyle = 'rgba(255, 184, 0, 0.4)';
                this.ctx.lineWidth = 1;
                this.ctx.beginPath();
                this.ctx.arc(node.x, node.y, radius + 10, 0, Math.PI * 2);
                this.ctx.stroke();
                this.ctx.shadowBlur = 0;
            }

            // Draw label
            this.ctx.fillStyle = '#e0e0e0';
            this.ctx.font = 'bold 11px "Courier New"';
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(node.label, node.x, node.y + radius + 18);

            // Draw status indicator
            if (node.status) {
                this.ctx.font = '9px "Courier New"';
                this.ctx.fillStyle = 'rgba(160, 160, 160, 0.8)';
                this.ctx.fillText(node.status.toUpperCase(), node.x, node.y + radius + 32);
            }
        });
    }

    drawBackground() {
        this.ctx.fillStyle = 'rgba(10, 14, 39, 0.8)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw grid
        this.ctx.strokeStyle = 'rgba(0, 212, 255, 0.05)';
        this.ctx.lineWidth = 1;
        const gridSize = 50;

        for (let x = 0; x < this.canvas.width; x += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        }

        for (let y = 0; y < this.canvas.height; y += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }
    }

    animate() {
        this.time += 0.016; // 60 FPS

        // Clear canvas
        this.drawBackground();

        // Draw edges and nodes
        this.drawEdges();
        this.drawNodes();

        // Continue animation
        this.animationFrame = requestAnimationFrame(() => this.animate());
    }

    destroy() {
        cancelAnimationFrame(this.animationFrame);
    }
}

// Initialize graph when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const graph = new SupplyChainGraph('graphCanvas');
});
