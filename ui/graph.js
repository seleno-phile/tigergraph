// Knowledge Graph Visualization Engine
class KnowledgeGraph {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        
        this.ctx = this.canvas.getContext('2d');
        this.nodes = [];
        this.edges = [];
        this.resize();
        window.addEventListener('resize', () => this.resize());
        this.animate();
    }

    resize() {
        this.canvas.width = this.canvas.parentElement.clientWidth;
        this.canvas.height = this.canvas.parentElement.clientHeight;
    }

    updateGraph(nodes, edges) {
        // Map backend nodes to visual nodes
        this.nodes = nodes.map(n => ({
            id: n.id,
            label: n.label,
            x: Math.random() * this.canvas.width,
            y: Math.random() * this.canvas.height,
            vx: 0,
            vy: 0,
            color: '#00d4ff'
        }));

        this.edges = edges.map(e => ({
            source: e.source,
            target: e.target,
            label: e.type
        }));
    }

    animate() {
        this.update();
        this.draw();
        requestAnimationFrame(() => this.animate());
    }

    update() {
        const k = 0.05; // Spring constant
        const repulsion = 1000;
        const damping = 0.9;

        // Apply forces
        for (let i = 0; i < this.nodes.length; i++) {
            let n1 = this.nodes[i];

            // Repulsion between nodes
            for (let j = i + 1; j < this.nodes.length; j++) {
                let n2 = this.nodes[j];
                let dx = n2.x - n1.x;
                let dy = n2.y - n1.y;
                let distSq = dx * dx + dy * dy || 1;
                let force = repulsion / distSq;
                let fx = (dx / Math.sqrt(distSq)) * force;
                let fy = (dy / Math.sqrt(distSq)) * force;
                n1.vx -= fx;
                n1.vy -= fy;
                n2.vx += fx;
                n2.vy += fy;
            }

            // Central attraction
            n1.vx += (this.canvas.width / 2 - n1.x) * 0.01;
            n1.vy += (this.canvas.height / 2 - n1.y) * 0.01;
        }

        // Attraction for edges
        this.edges.forEach(e => {
            let s = this.nodes.find(n => n.id === e.source);
            let t = this.nodes.find(n => n.id === e.target);
            if (s && t) {
                let dx = t.x - s.x;
                let dy = t.y - s.y;
                let dist = Math.sqrt(dx * dx + dy * dy);
                let force = (dist - 100) * k;
                let fx = (dx / dist) * force;
                let fy = (dy / dist) * force;
                s.vx += fx;
                s.vy += fy;
                t.vx -= fx;
                t.vy -= fy;
            }
        });

        // Update positions
        this.nodes.forEach(n => {
            n.vx *= damping;
            n.vy *= damping;
            n.x += n.vx;
            n.y += n.vy;

            // Keep in bounds
            n.x = Math.max(20, Math.min(this.canvas.width - 20, n.x));
            n.y = Math.max(20, Math.min(this.canvas.height - 20, n.y));
        });
    }

    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw edges
        this.ctx.strokeStyle = 'rgba(0, 212, 255, 0.2)';
        this.ctx.lineWidth = 1;
        this.edges.forEach(e => {
            let s = this.nodes.find(n => n.id === e.source);
            let t = this.nodes.find(n => n.id === e.target);
            if (s && t) {
                this.ctx.beginPath();
                this.ctx.moveTo(s.x, s.y);
                this.ctx.lineTo(t.x, t.y);
                this.ctx.stroke();
            }
        });

        // Draw nodes
        this.nodes.forEach(n => {
            this.ctx.fillStyle = n.color;
            this.ctx.beginPath();
            this.ctx.arc(n.x, n.y, 6, 0, Math.PI * 2);
            this.ctx.fill();

            this.ctx.fillStyle = '#a0a0a0';
            this.ctx.font = '10px Courier New';
            this.ctx.fillText(n.label, n.x + 10, n.y + 5);
        });
    }
}

// Global visualizer instance
document.addEventListener('DOMContentLoaded', () => {
    window.GraphVisualizer = new KnowledgeGraph('graphCanvas');
});
