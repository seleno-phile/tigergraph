/*
 * Supply Chain Intelligence Dashboard
 * Configuration and Constants
 * 
 * Edit this file to customize the dashboard behavior
 */

const DashboardConfig = {
    // Server Settings
    server: {
        host: 'localhost',
        port: 8000,
        apiEndpoint: '/api',  // Change to your backend API
    },

    // File Upload Settings
    upload: {
        maxFileSize: 500 * 1024 * 1024,  // 500MB in bytes
        allowedFormats: ['application/pdf', 'text/plain'],
        acceptExtensions: '.pdf,.txt',
    },

    // Graph Settings
    graph: {
        width: '100%',
        height: '100%',
        nodeRadius: 15,
        nodeRadiusHover: 20,
        nodeColor: {
            supplier: '#ffb800',
            facility: '#00d4ff',
            distribution: '#9d9dff',
            alternative: '#00ff88',
        },
        edgeWidth: 1,
        edgeColor: 'rgba(0, 212, 255, 0.3)',
        animationSpeed: 0.5,
        gridSize: 50,
    },

    // Query Settings
    query: {
        timeout: 5000,  // 5 seconds
        minLength: 1,
        maxLength: 500,
        debounceDelay: 300,
    },

    // UI Theme Colors
    theme: {
        primary: '#0a0e27',
        secondary: '#1a1f3a',
        tertiary: '#252d4a',
        accentCyan: '#00d4ff',
        accentOrange: '#ffb800',
        accentGreen: '#00ff88',
        accentRed: '#ff4444',
        textPrimary: '#e0e0e0',
        textSecondary: '#a0a0a0',
        textMuted: '#606080',
        border: '#2a3050',
    },

    // Animation Settings
    animation: {
        enabled: true,
        duration: 300,
        easing: 'ease-in-out',
        fps: 60,
    },

    // Logging
    debug: {
        enabled: false,  // Set to true for verbose logging
        logToConsole: true,
        logLevel: 'info',  // 'debug', 'info', 'warn', 'error'
    },

    // API Configuration (for production backend)
    api: {
        baseUrl: 'http://localhost:3001',  // Change to your backend
        endpoints: {
            query: '/api/query',
            upload: '/api/upload',
            documents: '/api/documents',
            graph: '/api/graph',
        },
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
    },

    // Demo Data
    demo: {
        enabled: true,  // Show demo supply chain
        nodes: [
            { id: 'nexacorp', label: 'NexaCorp', type: 'supplier', status: 'stable' },
            { id: 'vertexenergy', label: 'Vertex Energy', type: 'supplier', status: 'delayed' },
            { id: 'taiwanfacility', label: 'Taiwan Facility', type: 'facility', status: 'stable' },
            { id: 'altpowerinc', label: 'Alt-Power Inc', type: 'supplier', status: 'available' },
            { id: 'europeandistribution', label: 'European Distribution', type: 'distribution', status: 'blocked' },
            { id: 'assemblyph3', label: 'Assembly Ph.3', type: 'facility', status: 'delayed' },
        ],
        edges: [
            { from: 'nexacorp', to: 'taiwanfacility', label: 'Microprocessors' },
            { from: 'vertexenergy', to: 'taiwanfacility', label: 'Lithium Cells' },
            { from: 'taiwanfacility', to: 'assemblyph3', label: 'Assembly' },
            { from: 'assemblyph3', to: 'europeandistribution', label: 'Distribution' },
            { from: 'altpowerinc', to: 'taiwanfacility', label: 'Alt Supply' },
        ],
    },

    // Performance Settings
    performance: {
        maxNodes: 1000,
        maxEdges: 5000,
        enableWorkers: true,  // Use Web Workers for heavy computation
        cacheResults: true,
        cacheExpiry: 3600000,  // 1 hour in milliseconds
    },

    // Accessibility
    accessibility: {
        enableKeyboardShortcuts: true,
        enableScreenReaderSupport: true,
        highContrast: false,
    },

    // Storage
    storage: {
        useLocalStorage: true,
        useIndexedDB: false,
        storageKey: 'dashboard_data',
    },
};

// Helper function to get config value
function getConfig(path, defaultValue = null) {
    const keys = path.split('.');
    let value = DashboardConfig;
    
    for (let key of keys) {
        if (value && typeof value === 'object' && key in value) {
            value = value[key];
        } else {
            return defaultValue;
        }
    }
    
    return value;
}

// Helper function to update config
function setConfig(path, value) {
    const keys = path.split('.');
    const lastKey = keys.pop();
    let obj = DashboardConfig;
    
    for (let key of keys) {
        if (!(key in obj)) {
            obj[key] = {};
        }
        obj = obj[key];
    }
    
    obj[lastKey] = value;
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { DashboardConfig, getConfig, setConfig };
}
