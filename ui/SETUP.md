# 🚀 Supply Chain Intelligence Dashboard - Setup Guide

## Complete Installation & Running Guide

This guide will help you get the dashboard running on your Windows system in minutes.

---

## Prerequisites

### Required
- **Windows 7+** or any modern operating system
- **Python 3.7+** (free download from python.org)
- **Modern Web Browser** (Chrome, Firefox, Edge, Safari)
- **Internet Connection** (initially for setup)

### Optional
- **Node.js** (for http-server alternative)
- **Git** (already installed in your GitHub folder)

---

## Step 1: Verify Python Installation

### Check if Python is installed:

**Option A: Command Prompt**
```cmd
python --version
```

**Option B: PowerShell**
```powershell
python --version
```

Expected output: `Python 3.x.x`

### If Not Installed:

1. Visit https://www.python.org/downloads/
2. Download Python 3.9 or newer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"
5. Restart your computer
6. Try `python --version` again

---

## Step 2: Navigate to Project Directory

### Using Command Prompt:
```cmd
cd C:\Users\Asus\OneDrive\Documents\GitHub\tigergraph\ui
dir
```

You should see these files:
```
index.html
styles.css
dashboard.js
graph.js
config.js
server.py
start-server.bat
README.md
QUICKSTART.md
```

---

## Step 3: Start the Dashboard

### Method 1: One-Click (Easiest for Windows)

1. Open File Explorer
2. Navigate to: `C:\Users\Asus\OneDrive\Documents\GitHub\tigergraph\ui`
3. **Double-click** the file: `start-server.bat`
4. A black window will appear (the server)
5. Your browser should open automatically to `http://localhost:8000`

### Method 2: Command Prompt

```cmd
cd C:\Users\Asus\OneDrive\Documents\GitHub\tigergraph\ui
python server.py
```

Output should show:
```
============================================================
Supply Chain Intelligence Dashboard
============================================================

✓ Server running at: http://localhost:8000
✓ Serving files from: C:\Users\Asus\OneDrive\Documents\GitHub\tigergraph\ui

Press Ctrl+C to stop the server
```

Then open: **http://localhost:8000** in your browser

### Method 3: Python Built-in Server

```cmd
cd C:\Users\Asus\OneDrive\Documents\GitHub\tigergraph\ui
python -m http.server 8000
```

Then open: **http://localhost:8000**

### Method 4: Using Node.js (if installed)

```cmd
cd C:\Users\Asus\OneDrive\Documents\GitHub\tigergraph\ui
npx http-server
```

---

## Step 4: Access the Dashboard

Once the server is running, open your browser and visit:

### Primary: http://localhost:8000
### Alternative: http://127.0.0.1:8000
### Alternative: http://192.168.x.x:8000 (your machine IP)

You should see:
- Dark futuristic interface
- "SUPPLY CHAIN INTELLIGENCE" header
- Upload section on the left
- Analysis panel in the center
- Interactive graph on the right

---

## Step 5: Test the Dashboard

### 1. Test Upload
- Click the upload box on the left
- Select any text or PDF file from your computer
- See the progress bar and "INDEXED" status

### 2. Test Graph
- Look at the right panel
- You should see colorful nodes and connecting lines
- Hover over nodes to highlight them

### 3. Test Query
- Scroll down to find the query input box
- Type: "What are the main suppliers?"
- Press Enter or click the ⚡ button
- You should see a success notification

### 4. Check Metrics
- On the left sidebar, metrics should update as you upload files
- "Records Retrieved" and "Relevance Score" should change

---

## Port Configuration

### Default Port: 8000

If port 8000 is already in use:

**Command Prompt:**
```cmd
python server.py 3000
```

**Python Module:**
```cmd
python -m http.server 9000
```

Then open: `http://localhost:3000` or `http://localhost:9000`

---

## File Structure Explained

```
c:\Users\Asus\OneDrive\Documents\GitHub\tigergraph\ui\
│
├── index.html              ← Main page (open this in browser if server fails)
├── styles.css              ← Visual styling and theme
├── dashboard.js            ← Functionality and interactions
├── graph.js                ← Supply chain graph visualization
├── config.js               ← Configuration settings (customize here)
├── server.py               ← Development server (run this)
├── start-server.bat        ← Windows launcher script
│
├── README.md               ← Full documentation
├── QUICKSTART.md           ← Quick start guide
├── SETUP.md                ← This file
│
└── [demo data included]    ← Pre-loaded supply chain example
```

---

## Customization Guide

### Change Port in start-server.bat

Edit the last line:
```batch
python server.py 8000
```

Change `8000` to your desired port (e.g., `3000`)

### Change Dashboard Colors

Edit `config.js`:
```javascript
theme: {
    accentCyan: '#00d4ff',      // Main color
    accentOrange: '#ffb800',    // Supplier color
    accentGreen: '#00ff88',     // Alternative color
}
```

### Add Custom Supply Chain Data

Edit `config.js` in the `demo` section:
```javascript
demo: {
    enabled: true,
    nodes: [
        { id: 'mynode', label: 'My Supplier', type: 'supplier', status: 'stable' },
        // Add more nodes
    ],
    edges: [
        { from: 'node1', to: 'node2', label: 'Connection' },
        // Add more edges
    ]
}
```

---

## Troubleshooting

### Problem: "Python is not recognized"
**Solution:**
1. Download Python from python.org
2. Run installer
3. **CHECK** "Add Python to PATH"
4. Restart Command Prompt
5. Try again

### Problem: "Port 8000 already in use"
**Solution:**
```cmd
python server.py 9000
# Then open http://localhost:9000
```

### Problem: Black screen in browser
**Solution:**
1. Wait 2-3 seconds
2. Press F5 to refresh
3. Open DevTools (F12) to check for errors
4. Try a different browser

### Problem: Files can't find each other
**Solution:**
- Make sure you're using `http://localhost:8000`
- NOT `file://` protocol
- Run a proper server

### Problem: Graph not showing
**Solution:**
1. Check browser console (F12)
2. Look for JavaScript errors
3. Ensure HTML5 Canvas is supported
4. Try Chrome or Firefox

### Problem: Upload doesn't work
**Solution:**
1. Use `http://` not `file://`
2. Check file size (max 500MB)
3. Use PDF or TXT files only
4. Check browser console for errors

---

## Performance Tips

1. **Keep files under 100MB** for faster processing
2. **Use Chrome or Edge** for best performance
3. **Close other tabs** if running slow
4. **Restart browser** if memory builds up
5. **Use SSD** for better file access speeds

---

## Security Considerations

This dashboard is designed for **local development only**.

For **production deployment**:

1. Use HTTPS instead of HTTP
2. Add authentication/authorization
3. Implement rate limiting
4. Use environment variables for secrets
5. Validate all file uploads on server-side
6. Add CORS policies

Example production setup:
- Deploy to Nginx or Apache
- Use Docker for containerization
- Set up behind a proxy (HAProxy, Nginx)
- Use SSL certificates (Let's Encrypt)
- Implement user authentication

---

## Advanced Configuration

### Enable Debug Mode

Edit `config.js`:
```javascript
debug: {
    enabled: true,  // Shows detailed logs
    logToConsole: true,
    logLevel: 'debug',  // 'debug', 'info', 'warn', 'error'
}
```

### Change API Endpoint (for backend integration)

Edit `config.js`:
```javascript
api: {
    baseUrl: 'http://your-api.com',
    endpoints: {
        query: '/api/query',
        upload: '/api/upload',
    }
}
```

### Enable Web Workers (for large graphs)

Edit `config.js`:
```javascript
performance: {
    enableWorkers: true,
    maxNodes: 5000,  // Increase limit
}
```

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter | Execute query |
| Ctrl+R | Refresh browser |
| F12 | Open Developer Tools |
| Ctrl+Shift+I | Open Inspector |

---

## Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✅ Fully Supported |
| Edge | 90+ | ✅ Fully Supported |
| Firefox | 88+ | ✅ Fully Supported |
| Safari | 14+ | ✅ Fully Supported |
| Opera | 76+ | ✅ Fully Supported |
| IE 11 | Any | ❌ Not Supported |

---

## Next Steps

1. **Explore the Dashboard**
   - Upload sample files
   - Query the supply chain
   - Interact with the graph

2. **Customize Settings**
   - Edit `config.js` for your needs
   - Change colors and themes
   - Add your own supply chain data

3. **Connect to Backend** (Optional)
   - Modify API endpoints
   - Implement real data processing
   - Connect to your GraphRAG engine

4. **Deploy to Production** (Optional)
   - Use Docker or cloud platform
   - Set up HTTPS
   - Configure authentication

---

## Support & Help

### Quick Checks:
1. Is the server running? (Check for "Server running at..." message)
2. Is your browser using `http://` not `file://`?
3. Do you see console errors? (Press F12 in browser)
4. Have you tried a different browser?

### Check Browser Console:
1. Press F12
2. Click "Console" tab
3. Look for red error messages
4. Report or fix errors

---

## Stopping the Server

### Method 1: Command Prompt
Press `Ctrl+C` in the terminal window running the server

### Method 2: Windows Task Manager
1. Press `Ctrl+Shift+Esc`
2. Find "Python" process
3. Click "End Task"

### Method 3: Simply close the terminal window

---

## Updating the Dashboard

To get the latest version:

```cmd
cd C:\Users\Asus\OneDrive\Documents\GitHub\tigergraph
git pull origin main
```

Then restart the server.

---

## More Information

- **README.md** - Full feature documentation
- **QUICKSTART.md** - Quickstart guide
- **config.js** - Configuration reference
- Browser DevTools (F12) - For debugging
- Python console - Server logs and errors

---

## Final Checklist

- [ ] Python installed and in PATH
- [ ] All files present in ui/ folder
- [ ] Server running (black window visible)
- [ ] Browser shows dashboard at http://localhost:8000
- [ ] Upload box visible and clickable
- [ ] Graph visible on right side
- [ ] Query input box responsive
- [ ] Metrics updating

---

## 🎉 You're Ready!

The Supply Chain Intelligence Dashboard is now running on your system.

**Happy analyzing!** 🚀

---

**Need help?** Check the README.md or QUICKSTART.md files in the ui/ folder.

Last Updated: 2026-05-13
Version: 1.0.0
