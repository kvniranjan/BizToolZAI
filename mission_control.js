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

// YouTube Analytics - reads from pre-fetched JSON file (updated by cron)
function getYouTubeStats() {
    try {
        const data = fs.readFileSync('/root/.openclaw/workspace/yt_stats.json', 'utf8');
        return JSON.parse(data);
    } catch(e) {
        return { subscribers: 'N/A', totalViews: 'N/A', videoCount: 'N/A', videos: [], updated: 'N/A' };
    }
}

app.get('/', async (req, res) => {
    const ytStats = getYouTubeStats();
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

    const pipelineRows = contentApproval.map((row, idx) => {
        if (row.length < 4) return '';
        const isPublished = row[3].trim() === 'Published';
        let statusColor = isPublished ? 'bg-green-500/20 text-green-400' : 'bg-blue-500/20 text-blue-400';
        const draftFile = row[2] ? row[2].trim() : '';
        const toolName = row[1] ? row[1].trim() : '';
        const checkboxHtml = !isPublished
            ? '<input type="checkbox" class="pipeline-check w-4 h-4 rounded accent-blue-500 cursor-pointer" data-file="' + draftFile + '" data-tool="' + toolName + '" data-row="' + idx + '">'
            : '<span class="text-green-500 text-xs">&#10003;</span>';
        const fileBasename = draftFile.replace('content/', '');
        const toolLink = draftFile
            ? '<a href="/draft/' + fileBasename + '" target="_blank" class="hover:text-blue-400 transition-colors">' + toolName + ' &#8599;</a>'
            : toolName;
        const deleteBtn = !isPublished
            ? '<button onclick="deleteDraft(\'' + draftFile + '\',\'' + toolName.replace(/'/g, "\\'") + '\')" class="px-2.5 py-1 bg-red-600/20 hover:bg-red-600/40 text-red-400 hover:text-red-300 text-xs font-semibold rounded-lg border border-red-500/30 transition-colors">Delete</button>'
            : '';

        return '<tr class="border-b border-slate-800/50 hover:bg-slate-800/20 transition-colors" id="row-' + idx + '">' +
            '<td class="py-3 px-4">' + checkboxHtml + '</td>' +
            '<td class="py-3 px-4 text-slate-300 text-sm">' + row[0] + '</td>' +
            '<td class="py-3 px-4 text-white font-medium">' + toolLink + '</td>' +
            '<td class="py-3 px-4 text-slate-400 text-xs truncate max-w-[120px]">' + draftFile + '</td>' +
            '<td class="py-3 px-4"><span class="px-2.5 py-1 rounded-full text-xs font-semibold ' + statusColor + '">' + row[3].trim() + '</span></td>' +
            '<td class="py-3 px-4">' + deleteBtn + '</td>' +
            '</tr>';
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

        <!-- YouTube Analytics Banner -->
        <div class="glass-card rounded-2xl p-6 mb-8 border border-red-500/20">
            <div class="flex flex-col md:flex-row items-start md:items-center gap-6">
                <div class="flex items-center gap-3">
                    <svg class="w-8 h-8 text-red-500" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                    <div>
                        <h2 class="text-lg font-bold text-white">Obscured History</h2>
                        <a href="https://youtube.com/@ObscuredhistoryOfficial" target="_blank" class="text-xs text-red-400 hover:text-red-300">@ObscuredhistoryOfficial ↗</a>
                    </div>
                </div>
                <div class="flex flex-wrap gap-6 md:ml-auto">
                    <div class="text-center">
                        <p class="text-2xl font-extrabold text-white">${ytStats.subscribers}</p>
                        <p class="text-xs text-slate-400 uppercase tracking-wider">Subscribers</p>
                    </div>
                    <div class="text-center">
                        <p class="text-2xl font-extrabold text-white">${ytStats.totalViews}</p>
                        <p class="text-xs text-slate-400 uppercase tracking-wider">Total Views</p>
                    </div>
                    <div class="text-center">
                        <p class="text-2xl font-extrabold text-white">${ytStats.videoCount}</p>
                        <p class="text-xs text-slate-400 uppercase tracking-wider">Videos</p>
                    </div>
                </div>
            </div>
            ${ytStats.videos.length > 0 ? `
            <div class="mt-4 pt-4 border-t border-slate-800/50">
                <p class="text-xs text-slate-500 uppercase tracking-wider mb-3">Recent Videos</p>
                <div class="space-y-2">
                    ${ytStats.videos.map(v => `
                    <div class="flex justify-between items-center text-sm">
                        <span class="text-slate-300 truncate max-w-[60%]">${v.title}</span>
                        <div class="flex gap-4 text-xs text-slate-500">
                            <span>👁 ${Number(v.views).toLocaleString()}</span>
                            <span>👍 ${Number(v.likes).toLocaleString()}</span>
                            <span>💬 ${Number(v.comments).toLocaleString()}</span>
                        </div>
                    </div>`).join('')}
                </div>
            </div>` : ''}
        </div>

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
                        <div class="px-4 py-3 flex items-center gap-3 border-b border-slate-800/30 bg-slate-900/20">
                            <input type="checkbox" id="select-all" class="w-4 h-4 rounded accent-blue-500 cursor-pointer">
                            <label for="select-all" class="text-xs text-slate-400 cursor-pointer select-none">Select All</label>
                            <button onclick="publishSelected()" id="publish-btn"
                                class="ml-auto px-4 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-lg transition-colors disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-2">
                                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>
                                Publish Selected
                            </button>
                        </div>
                        <div id="publish-result" class="hidden px-4 py-2 text-sm font-medium"></div>
                        <table class="w-full text-left border-collapse">
                            <thead>
                                <tr class="bg-slate-900/50 text-slate-400 text-xs uppercase tracking-wider">
                                    <th class="py-3 px-4 font-semibold w-8"></th>
                                    <th class="py-3 px-4 font-semibold">Date</th>
                                    <th class="py-3 px-4 font-semibold">Tool Name</th>
                                    <th class="py-3 px-4 font-semibold">Draft File</th>
                                    <th class="py-3 px-4 font-semibold">Status</th>
                                    <th class="py-3 px-4 font-semibold">Action</th>
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

        // Select all checkbox
        document.getElementById('select-all').addEventListener('change', function() {
            document.querySelectorAll('.pipeline-check').forEach(cb => cb.checked = this.checked);
        });

        async function deleteDraft(file, tool) {
            if (!confirm('Delete "' + tool + '" draft and remove from pipeline?\n\nThis cannot be undone.')) return;
            const res = await fetch('/delete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ file, tool })
            });
            const data = await res.json();
            if (data.success) {
                location.reload();
            } else {
                alert('Delete failed: ' + data.message);
            }
        }

        async function publishSelected() {
            const checked = [...document.querySelectorAll('.pipeline-check:checked')];
            if (checked.length === 0) {
                alert('Please select at least one draft to publish.');
                return;
            }

            const files = checked.map(cb => ({ file: cb.dataset.file, tool: cb.dataset.tool }));
            const btn = document.getElementById('publish-btn');
            btn.textContent = 'Publishing...';
            btn.disabled = true;

            const result = document.getElementById('publish-result');
            result.className = 'px-4 py-2 text-sm font-medium text-blue-400 bg-blue-500/10 border-b border-slate-800/30';
            result.textContent = 'Running publisher for ' + files.length + ' item(s)...';
            result.classList.remove('hidden');

            try {
                const res = await fetch('/publish', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ items: files })
                });
                const data = await res.json();
                if (data.success) {
                    result.className = 'px-4 py-2 text-sm font-medium text-green-400 bg-green-500/10 border-b border-slate-800/30';
                    result.textContent = '✅ ' + data.message;
                    setTimeout(() => location.reload(), 2000);
                } else {
                    result.className = 'px-4 py-2 text-sm font-medium text-red-400 bg-red-500/10 border-b border-slate-800/30';
                    result.textContent = '❌ ' + data.message;
                    btn.textContent = 'Publish Selected';
                    btn.disabled = false;
                }
            } catch(e) {
                result.textContent = '❌ Network error: ' + e.message;
                btn.textContent = 'Publish Selected';
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>`;

    res.send(html);
});

// Delete endpoint
app.post('/delete', (req, res) => {
    const { file, tool } = req.body;
    if (!file) return res.json({ success: false, message: 'No file specified' });

    try {
        // Delete the MD file
        const filePath = file.startsWith('content/') ? file : `content/${file}`;
        if (fs.existsSync(filePath)) {
            fs.unlinkSync(filePath);
        }

        // Remove from CSV
        const csvPath = 'content_approval.csv';
        const lines = fs.readFileSync(csvPath, 'utf8').split('\n');
        const filtered = lines.filter(line => !line.includes(file) || line.startsWith('Date,'));
        fs.writeFileSync(csvPath, filtered.join('\n'));

        console.log(`Deleted: ${filePath}`);
        res.json({ success: true, message: `Deleted ${tool}` });
    } catch(e) {
        res.json({ success: false, message: e.message });
    }
});

// Publish endpoint
app.use(express.json());
app.post('/publish', async (req, res) => {
    const { items } = req.body;
    if (!items || items.length === 0) {
        return res.json({ success: false, message: 'No items selected' });
    }

    const { execSync } = require('child_process');
    const results = [];

    for (const item of items) {
        if (!item.file) continue;
        try {
            // Run the publisher script for this specific file
            const cmd = `cd /root/.openclaw/workspace && /root/.openclaw/workspace/venv/bin/python3 auto_publisher.py "${item.file}" 2>&1`;
            const output = execSync(cmd, { timeout: 60000 }).toString().trim();
            results.push({ file: item.file, status: 'ok', output: output.slice(-200) });
        } catch(e) {
            results.push({ file: item.file, status: 'error', output: e.message.slice(-200) });
        }
    }

    const failed = results.filter(r => r.status === 'error');
    if (failed.length === 0) {
        res.json({ success: true, message: `Published ${results.length} item(s) successfully! Refreshing...` });
    } else {
        res.json({ success: false, message: `${results.length - failed.length} published, ${failed.length} failed. Check logs.` });
    }
});

app.listen(PORT, async () => {
    console.log(`Server restarted on port ${PORT}`);
});
