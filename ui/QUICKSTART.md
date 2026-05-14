# Quick Start Guide - Supply Chain Intelligence Dashboard

## 🚀 Getting Started in 30 Seconds

### Option 1: Windows (Easiest)
1. **Double-click** `start-server.bat` in the ui folder
2. Your browser should open to `http://localhost:8000` automatically
3. Done! The dashboard is ready to use

### Option 2: Python Command Line
```bash
cd c:\Users\Asus\OneDrive\Documents\GitHub\tigergraph\ui
python server.py
```
Then open: **http://localhost:8000**

### Option 3: Python Direct (No Custom Server)
```bash
cd c:\Users\Asus\OneDrive\Documents\GitHub\tigergraph\ui
python -m http.server 8000
```
Then open: **http://localhost:8000**

---

## 📁 What You Have

```
ui/
├── index.html           ← Main dashboard page
├── styles.css           ← Beautiful dark theme styling
├── dashboard.js         ← Upload, query, metrics logic
├── graph.js             ← Interactive supply chain graph
├── server.py            ← Python development server
├── start-server.bat     ← Windows launcher (one-click!)
├── README.md            ← Full documentation
└── QUICKSTART.md        ← This file
```

---

## 🎯 Features Ready to Use

### 1. **Upload Documents**
   - Click the upload box on the left
   - Drag & drop or select PDF/TXT files
   - Automatically indexed and tracked

### 2. **Interactive Graph**
   - View supply chain relationships on the right
   - Colored nodes: Orange (suppliers), Cyan (facilities), Purple (distribution)
   - Red borders show delayed items
   - Click nodes to select them

### 3. **Query System**
   - Type questions about your supply chain
   - Press Enter or click ⚡ button
   - Get instant analysis and insights

### 4. **Real-time Metrics**
   - Records retrieved count
   - Relevance score
   - Document indexing status

---

## 🔧 Customization

### Change Port
```bash
python server.py 3000  # Uses port 3000 instead
```

### Change Colors
Edit `styles.css` root variables:
```css
:root {
    --accent-cyan: #00d4ff;      /* Main accent color */
    --accent-orange: #ffb800;    /* Supplier/delayed color */
    --accent-green: #00ff88;     /* Alternative/available color */
}
```

### Add More Nodes
Edit `graph.js` `initializeGraph()` method:
```javascript
this.nodes = [
    { id: 'newnode', label: 'New Supplier', type: 'supplier', x: 150, y: 200, color: '#ffb800', status: 'stable' },
    // ... more nodes
];
```

---

## 🐛 Troubleshooting

**Port Already in Use?**
```bash
python server.py 9000  # Try different port
```

**Black screen?**
- Wait 2-3 seconds for canvas to load
- Press F12 to check browser console
- Try a different browser

**File upload not working?**
- Ensure you're using http:// (not file://)
- Check file size (max 500MB)
- Verify file is PDF or TXT

**Graph not showing?**
- Check browser supports HTML5 Canvas
- Try Chrome/Edge if using old browser
- Refresh the page (Ctrl+R)

---

## 📊 Demo Scenario (What You See)

The dashboard comes pre-loaded with a realistic supply chain example:

**Project Alpha Supply Chain:**
- **Suppliers**: NexaCorp (microprocessors), Vertex Energy (lithium cells)
- **Problem**: Vertex Energy is delayed ⚠️
- **Impact**: Assembly Phase 3 blocked, European distribution will miss Q3 deadline
- **Solution**: Reroute to Alt-Power Inc as alternative supplier

Try querying: *"What are the critical delays?"* or *"What suppliers can we use?"*

---

## 🚢 Production Deployment

To connect to a real backend:

1. **Backend API Setup** (Node.js, Python, Java, etc.)
2. **Modify `dashboard.js`** - Update `executeQuery()` to call your API:
   ```javascript
   async executeQuery() {
       const response = await fetch('http://your-api.com/query', {
           method: 'POST',
           body: JSON.stringify({ query: this.queryInput.value })
       });
       const data = await response.json();
       this.displayResults(data);
   }
   ```
3. **Deploy to web server** (Nginx, Apache, etc.)

---

## 📚 File Descriptions

| File | Purpose |
|------|---------|
| `index.html` | Page structure - upload, analysis, graph |
| `styles.css` | Cyberpunk styling - colors, layout, animations |
| `dashboard.js` | Business logic - uploads, queries, metrics |
| `graph.js` | Graph rendering - nodes, edges, physics |
| `server.py` | Local development server |
| `start-server.bat` | Windows one-click launcher |

---

## 🎨 UI Layout

```
┌─────────────────────────────────────────────────────────┐
│ SUPPLY CHAIN INTELLIGENCE | SYSTEM: ONLINE              │
├──────────────┬────────────────────────────────┬──────────┤
│   UPLOAD     │     ANALYSIS & INSIGHTS       │  GRAPH   │
│  DOCUMENTS   │  (RAG Engine Results)         │ VISUAL   │
│              │                                │          │
│ Active Docs  │  • Primary Dependencies       │ Nodes:   │
│ • Alpha.pdf  │  • Critical Path Analysis    │ 6 nodes  │
│ • Logistics  │  • Secondary Impact           │ Colored  │
│              │  • Recommended Action         │ Network  │
│ Metrics      │  • Query Results              │          │
│ 1.2K records │                              │          │
│ 84% score    │  [Query Box]                 │          │
└──────────────┴────────────────────────────────┴──────────┘
```

---

## 💡 Tips & Tricks

1. **Drag files** onto the upload box instead of clicking
2. **Press Enter** to query faster than clicking the button
3. **Hover over nodes** in the graph to highlight them
4. **Click nodes** to select and focus on specific parts
5. **Watch metrics** update as you upload documents
6. **Dark mode is built-in** - perfect for late night work! 🌙

---

## 🌐 Browser Support

✅ Chrome/Edge 90+
✅ Firefox 88+
✅ Safari 14+
✅ Opera 76+
❌ Internet Explorer (not supported)

---

## 📞 Need Help?

1. Check the full README.md for detailed documentation
2. Open browser DevTools (F12) to see console errors
3. Try a different browser
4. Restart the server

---

## 🎉 Ready!

Your Supply Chain Intelligence Dashboard is ready to use!

**Start the server and open:** http://localhost:8000

Good luck! 🚀
