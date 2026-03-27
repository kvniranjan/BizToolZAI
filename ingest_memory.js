const fs = require('fs');
const path = require('path');
const http = require('http');

async function ingest() {
    const memoryDir = 'memory';
    const files = fs.readdirSync(memoryDir).filter(f => f.endsWith('.md'));
    
    for (let f of files) {
        const filePath = path.join(memoryDir, f);
        const content = fs.readFileSync(filePath, 'utf8');
        
        console.log(`Ingesting ${f}...`);
        
        // Use the claude-mem REST API to store an observation
        const data = JSON.stringify({
            narrative: `Context from ${f}:\n${content}`,
            topics: ["memory_migration", "biztoolzai", f.replace('.md', '')],
            category: "memory"
        });

        const options = {
            hostname: '127.0.0.1',
            port: 37777,
            path: '/api/memory/observations',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': data.length
            }
        };

        const req = http.request(options, res => {
            console.log(`Status for ${f}: ${res.statusCode}`);
        });

        req.on('error', error => {
            console.error(`Error ingesting ${f}:`, error);
        });

        req.write(data);
        req.end();
        
        // Wait a sec between requests
        await new Promise(r => setTimeout(r, 1000));
    }
}
ingest();
