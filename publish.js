const fs = require('fs');

// 1. Convert ElevenLabs to HTML
const mdContent = fs.readFileSync('content/ElevenLabs_2026-05-07.md', 'utf-8');
const titleMatch = mdContent.match(/\*\*Title:\*\* (.*?)\n/);
const descMatch = mdContent.match(/\*\*Meta Description:\*\* (.*?)\n/);
const bodyMatch = mdContent.split('**Review Body:**\n')[1].split('\n## Social Content')[0].trim();
const pBody = bodyMatch.split('\n\n').map(p => `<p class="mb-4">${p}</p>`).join('\n');

const title = titleMatch ? titleMatch[1] : "ElevenLabs Review 2026";
const desc = descMatch ? descMatch[1] : "ElevenLabs Review";

const blogHtml = `<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="${desc}">
    <title>${title} — BizToolz AI</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: { sans: ['"Plus Jakarta Sans"', 'sans-serif'] },
                    colors: { primary: '#0369A1', card: '#FFFFFF', border: '#E2E8F0', foreground: '#020617', 'muted-foreground': '#64748B' }
                }
            }
        }
    </script>
</head>
<body class="antialiased font-sans bg-slate-50 text-slate-900">
    <nav class="fixed w-full top-0 z-50 bg-white/90 backdrop-blur border-b border-slate-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between h-16 items-center">
            <a href="/" class="font-bold text-xl flex items-center gap-2"><span>⚡</span> BizToolz AI</a>
            <div class="space-x-8">
                <a href="/blog/" class="text-primary font-medium">Reviews</a>
            </div>
        </div>
    </nav>
    <main class="pt-32 pb-16 max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="mb-8 flex items-center gap-4">
            <img src="https://logo.clearbit.com/elevenlabs.io" class="w-16 h-16 rounded-xl border border-slate-200 shadow-sm" onerror="this.style.display='none'">
            <h1 class="text-4xl font-extrabold tracking-tight">${title}</h1>
        </div>
        <div class="prose prose-slate lg:prose-lg text-slate-600 leading-relaxed">
            ${pBody}
        </div>
    </main>
</body>
</html>`;

fs.writeFileSync('blog/elevenlabs.html', blogHtml);

// 2. Update blog/index.html
let indexHtml = fs.readFileSync('blog/index.html', 'utf-8');
const newCard = `
            <a href="elevenlabs.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-bold text-primary uppercase tracking-wider">Audio Generators</span>
                    <img src="https://logo.clearbit.com/elevenlabs.io?size=64" onerror="this.style.display='none'" class="w-8 h-8 rounded-md shadow-sm border border-border object-cover" alt="ElevenLabs Logo">
                </div>
                <h3 class="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">${title}</h3>
                <p class="text-muted-foreground text-sm mb-6 flex-grow">${desc.substring(0, 100)}...</p>
                <div class="flex justify-between items-center text-sm font-semibold text-secondary pt-4 border-t border-border">
                    <span>📖 4 min read</span>
                    <span>🚀 New</span>
                </div>
            </a>
`;
indexHtml = indexHtml.replace('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">', '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">\n' + newCard);
fs.writeFileSync('blog/index.html', indexHtml);

// 3. Update Hub (Audio Generators)
const hubDir = 'use-cases';
if (!fs.existsSync(hubDir)) fs.mkdirSync(hubDir);
const hubPath = `${hubDir}/audio-generators.html`;
let hubHtml = `<!DOCTYPE html><html><head><title>Audio Generators Hub</title></head><body><h1>Audio Generators</h1><div id="cards"></div></body></html>`;
if (fs.existsSync(hubPath)) hubHtml = fs.readFileSync(hubPath, 'utf-8');
hubHtml = hubHtml.replace('<div id="cards">', '<div id="cards">\n' + newCard);
fs.writeFileSync(hubPath, hubHtml);

// Hub Index update
const hubIndex = `${hubDir}/index.html`;
let hubIndexHtml = fs.existsSync(hubIndex) ? fs.readFileSync(hubIndex, 'utf-8') : '<ul></ul>';
if (!hubIndexHtml.includes('audio-generators.html')) {
    hubIndexHtml = hubIndexHtml.replace('<ul>', '<ul>\n<li><a href="audio-generators.html">Audio Generators</a></li>');
    fs.writeFileSync(hubIndex, hubIndexHtml);
}

// 4. Update CSV
let csv = fs.readFileSync('content_approval.csv', 'utf-8');
csv = csv.replace('2026-05-07,ElevenLabs,content/ElevenLabs_2026-05-07.md,Auto-Queue', '2026-05-07,ElevenLabs,content/ElevenLabs_2026-05-07.md,Published');
fs.writeFileSync('content_approval.csv', csv);

