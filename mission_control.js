const express = require('express');
const fs = require('fs');
const path = require('path');
const admin = require('firebase-admin');
const { marked } = require('marked');

try {
    if (!admin.apps.length) {
        const serviceAccount = require('./serviceAccountKey.json');
        admin.initializeApp({
          credential: admin.credential.cert(serviceAccount)
        });
    }
} catch (e) {
    console.error("Firebase init failed:", e.message);
}

const app = express();
const PORT = 3030;

function safeRead(file) {
    try { return fs.readFileSync(file, 'utf8'); } catch(e) { return ''; }
}

function parseCSV(csvText) {
    if (!csvText) return [];
    const lines = csvText.trim().split('\n');
    return lines.map(line => line.split(','));
}

// 0. Static image serving
app.get('/images/:filename', (req, res) => {
    const filename = path.basename(req.params.filename);
    const filepath = path.join('/root/.openclaw/workspace/videos/images', filename);
    if (!fs.existsSync(filepath)) return res.status(404).send('Not found');
    res.setHeader('Content-Type', 'image/png');
    fs.createReadStream(filepath).pipe(res);
});

// 0b. Video serving route
app.get("/video/:filename", (req, res) => {
    const filename = path.basename(req.params.filename);
    const filepath = path.join("/root/.openclaw/workspace/videos/final", filename);
    if (!fs.existsSync(filepath)) return res.status(404).send("Not found");
    res.setHeader("Content-Type", "video/mp4");
    res.setHeader("Content-Disposition", "attachment; filename=\"" + filename + "\"");
    fs.createReadStream(filepath).pipe(res);
});

// 1. Single Draft Viewer Route
app.get('/draft/:filename', (req, res) => {
    const filename = path.basename(req.params.filename);
    const filepath = path.join('content', filename);

    if (!fs.existsSync(filepath) || !filename.endsWith('.md')) {
        return res.status(404).send("<h1 style='color:white; font-family:sans-serif;'>Draft not found.</h1>");
    }

    const mdContent = fs.readFileSync(filepath, 'utf8');
    const htmlContent = marked.parse(mdContent);

    const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Draft: ${filename}</title>
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #020617; color: #f8fafc; }
        .glass-card { background: linear-gradient(145deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.8)); backdrop-filter: blur(16px); border: 1px solid rgba(51, 65, 85, 0.5); }
    </style>
</head>
<body class="min-h-screen py-10 px-4 sm:px-8 relative">
    <div class="fixed top-[-20%] left-[-10%] w-[50%] h-[50%] bg-blue-600/10 blur-[120px] rounded-full pointer-events-none"></div>
    
    <div class="w-full max-w-4xl mx-auto z-10 relative">
        <a href="/" class="inline-block text-blue-400 hover:text-blue-300 font-semibold mb-8 flex items-center gap-2">
            <span>&larr;</span> Back to Mission Control
        </a>
        
        <div class="glass-card p-8 sm:p-12 rounded-3xl shadow-xl">
            <div class="flex items-center gap-3 mb-8 pb-6 border-b border-slate-700/50">
                <span class="text-3xl">📄</span>
                <div>
                    <h1 class="text-xl font-bold text-white tracking-tight">${filename}</h1>
                    <p class="text-sm text-slate-400">Raw Markdown converted to HTML</p>
                </div>
            </div>
            
            <article class="prose prose-invert prose-slate prose-lg max-w-none prose-a:text-blue-400 hover:prose-a:text-blue-300">
                ${htmlContent}
            </article>
        </div>
    </div>
</body>
</html>`;

    res.send(html);
});

// 2. Main Dashboard Route
app.get('/', async (req, res) => {
    const contentApprovalRaw = safeRead('content_approval.csv');
    const contentApproval = parseCSV(contentApprovalRaw).filter(r => r.length > 1).reverse().slice(0, 8);
    
    const affiliateLogRaw = safeRead('affiliate_log.csv');
    const affiliateLog = parseCSV(affiliateLogRaw).filter(r => r.length > 1).reverse().slice(0, 6);
    
    // Read the specific Reddit Leads file and convert it to HTML immediately
    const redditLeadsRaw = safeRead('content/reddit_leads.md');
    const redditLeadsHTML = redditLeadsRaw ? marked.parse(redditLeadsRaw) : '<p class="text-slate-400 italic text-sm">No Reddit leads generated today. The scout runs at 10 AM EST.</p>';

    let contentFiles = [];
    try {
        contentFiles = fs.readdirSync('content')
            .filter(f => f.endsWith('.md') && f !== 'reddit_leads.md')
            .map(file => {
                const stats = fs.statSync(path.join('content', file));
                return { name: file, time: stats.mtime };
            })
            .sort((a, b) => b.time - a.time)
            .slice(0, 6);
    } catch(e) {}

    let publishedCount = 0;
    try {
        publishedCount = fs.readdirSync('blog').filter(f => f.endsWith('.html') && f !== 'index.html').length;
    } catch(e) {}

    let subCount = "Loading...";
    try {
        if (admin.apps.length) {
            const db = admin.firestore();
            const subSnap = await db.collection('subscribers').count().get();
            subCount = subSnap.data().count;
        } else {
            subCount = "N/A";
        }
    } catch (e) {
        subCount = "Error";
    }

    const pipelineRows = contentApproval.map(row => {
        if (row.length < 4) return '';
        let statusColor = row[3].trim() === 'Published' ? 'bg-green-500/20 text-green-400' : 'bg-blue-500/20 text-blue-400';
        return `
        <tr class="border-b border-slate-800/50 hover:bg-slate-800/20 transition-colors">
            <td class="py-3 px-4 text-slate-300 text-sm">${row[0]}</td>
            <td class="py-3 px-4 text-white font-medium">${row[1]}</td>
            <td class="py-3 px-4 text-slate-400 text-xs truncate max-w-[150px]">${row[2]}</td>
            <td class="py-3 px-4"><span class="px-2.5 py-1 rounded-full text-xs font-semibold ${statusColor}">${row[3]}</span></td>
        </tr>`;
    }).join('');

    const filesRows = contentFiles.map(f => `
        <li class="flex items-center gap-3 text-sm hover:bg-slate-800/30 p-2 rounded-lg transition-colors cursor-pointer" onclick="window.location.href='/draft/${f.name}'">
            <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            <span class="truncate font-medium text-slate-300 hover:text-white transition-colors">${f.name}</span>
            <span class="ml-auto text-xs text-slate-500">Read &rarr;</span>
        </li>
    `).join('');

    const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BizToolz Mission Control 🚀</title>
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #020617; color: #f8fafc; }
        .glass-card { background: linear-gradient(145deg, rgba(30, 41, 59, 0.4), rgba(15, 23, 42, 0.6)); backdrop-filter: blur(16px); border: 1px solid rgba(51, 65, 85, 0.5); box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1); }
        .stat-gradient { background: linear-gradient(to right, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center py-10 px-4 sm:px-8 relative overflow-x-hidden">
    <div class="fixed top-[-20%] left-[-10%] w-[50%] h-[50%] bg-blue-600/10 blur-[120px] rounded-full pointer-events-none"></div>
    <div class="fixed bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-purple-600/10 blur-[120px] rounded-full pointer-events-none"></div>

    <div class="w-full max-w-7xl z-10">
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-4">
            <div>
                <h1 class="text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
                    <span class="text-blue-500">⚡</span> BizToolz Operations
                </h1>
                <p class="text-slate-400 mt-1 text-sm font-medium">Live Node Analytics & Autonomous Systems</p>
            </div>
            <div class="glass-card px-4 py-2 rounded-full flex items-center gap-3">
                <span class="relative flex h-2.5 w-2.5">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                </span>
                <span class="text-slate-300 font-bold uppercase tracking-widest text-xs">System Online</span>
            </div>
        </header>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div class="glass-card p-6 rounded-2xl">
                <h3 class="text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">Live Subscribers</h3>
                <p class="text-4xl font-extrabold stat-gradient">${subCount}</p>
                <p class="text-xs text-emerald-400 mt-2 font-medium">↑ Verified via Firebase</p>
            </div>
            <div class="glass-card p-6 rounded-2xl">
                <h3 class="text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">Published Reviews</h3>
                <p class="text-4xl font-extrabold stat-gradient">${publishedCount}</p>
                <p class="text-xs text-blue-400 mt-2 font-medium">↑ Indexed in Sitemap</p>
            </div>
            <div class="glass-card p-6 rounded-2xl">
                <h3 class="text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">Sniper Bot Status</h3>
                <p class="text-2xl font-extrabold text-white mt-1">Watching [CALM]</p>
                <p class="text-xs text-slate-400 mt-2 font-medium">Stop Loss: $70.98</p>
            </div>
            <div class="glass-card p-6 rounded-2xl">
                <h3 class="text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">Next Auto-Publish</h3>
                <p class="text-2xl font-extrabold text-white mt-1">10:00 PM UTC</p>
                <p class="text-xs text-slate-400 mt-2 font-medium">Cron Schedule Active</p>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <div class="space-y-8 flex flex-col lg:col-span-2">
                <!-- Reddit Leads Box -->
                <div class="glass-card rounded-3xl p-8 flex-grow shadow-2xl relative overflow-hidden">
                    <div class="absolute top-0 right-0 bg-orange-600/20 text-orange-400 text-xs font-bold px-4 py-2 rounded-bl-xl border-l border-b border-orange-500/30">
                        Updates Daily @ 10 AM EST
                    </div>
                    <h2 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
                        <span class="text-orange-500 text-2xl">👽</span> Today's Reddit Targets
                    </h2>
                    <div class="bg-slate-900/60 p-6 rounded-2xl border border-slate-700/50 max-h-[500px] overflow-y-auto custom-scrollbar">
                        <div class="prose prose-invert prose-sm prose-slate max-w-none prose-headings:text-orange-400 prose-a:text-blue-400">
                            ${redditLeadsHTML}
                        </div>
                    </div>
                </div>

                <!-- Publishing Pipeline -->
                <div class="glass-card rounded-3xl overflow-hidden flex flex-col">
                    <div class="p-6 border-b border-slate-800/50 bg-slate-900/30">
                        <h2 class="text-lg font-bold text-white flex items-center gap-2">
                            <span class="text-blue-400">📝</span> Publishing Pipeline
                        </h2>
                    </div>
                    <div class="overflow-x-auto flex-grow p-0">
                        <table class="w-full text-left border-collapse">
                            <thead>
                                <tr class="bg-slate-900/50 text-slate-400 text-xs uppercase tracking-wider">
                                    <th class="py-3 px-4 font-semibold">Date</th>
                                    <th class="py-3 px-4 font-semibold">Tool Name</th>
                                    <th class="py-3 px-4 font-semibold">Draft File</th>
                                    <th class="py-3 px-4 font-semibold">Status</th>
                                </tr>
                            </thead>
                            <tbody class="align-baseline">
                                ${pipelineRows}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="space-y-8 flex flex-col">
                <div class="glass-card rounded-3xl p-6 flex-grow">
                    <h2 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
                        <span class="text-purple-400">📄</span> Active Drafts
                    </h2>
                    <p class="text-xs text-slate-400 mb-4">Click to view formatted HTML preview.</p>
                    <ul class="space-y-1">
                        ${filesRows}
                    </ul>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        setTimeout(() => location.reload(), 60000);
    </script>
</body>
</html>`;

    res.send(html);
});

app.listen(PORT, async () => {
    console.log(`Server restarted on port ${PORT}`);
});
