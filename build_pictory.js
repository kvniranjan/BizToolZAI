const fs = require('fs');
const text = fs.readFileSync('content/Pictory_2026-05-09.md', 'utf8');

const titleMatch = text.match(/## Title\n(.*?)\n/);
const title = titleMatch ? titleMatch[1].trim() : 'Pictory AI Review';

const metaMatch = text.match(/## Meta Description\n(.*?)\n/);
const meta = metaMatch ? metaMatch[1].trim() : '';

const bodyStart = text.indexOf('## Review Body');
let bodyText = text.substring(bodyStart + '## Review Body'.length).trim();

// Super simple markdown to HTML replacement for the subset used here
let bodyHtml = bodyText
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>')
    .replace(/^- (.*$)/gim, '<ul><li>$1</li></ul>')
    .replace(/<\/ul>\n<ul>/gim, '\n') // merge adjacent lists
    .replace(/\n\n/gim, '</p><p>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2">$1</a>');

bodyHtml = '<p>' + bodyHtml + '</p>';
// fix standalone headers inside <p>
bodyHtml = bodyHtml.replace(/<p><h/g, '<h').replace(/<\/h2><\/p>/g, '</h2>').replace(/<\/h3><\/p>/g, '</h3>');
bodyHtml = bodyHtml.replace(/<p><ul/g, '<ul').replace(/<\/ul><\/p>/g, '</ul>');

const template = `<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="${meta}">
    <title>${title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #F8FAFC; color: #020617; }
        .glass-nav { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(12px); border-bottom: 1px solid #E2E8F0; }
    </style>
</head>
<body class="antialiased font-sans">
    <nav class="glass-nav fixed w-full top-0 z-50 transition-all duration-300">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16 items-center">
                <div class="flex-shrink-0 flex items-center gap-2">
                    <span class="text-2xl">⚡</span>
                    <a href="/" class="font-bold text-xl tracking-tight text-foreground hover:text-primary transition-colors">BizToolz AI</a>
                </div>
                <div class="hidden md:flex space-x-8 items-center">
                    <a href="/#tools" class="text-muted-foreground hover:text-primary font-medium transition-colors">Top Tools</a>
                    <a href="/use-cases/" class="text-muted-foreground hover:text-primary font-medium transition-colors">Use Cases</a>
                    <a href="/blog/" class="text-primary font-medium transition-colors">Reviews</a>
                    <a href="#newsletter" class="bg-primary hover:bg-primary-hover text-white px-5 py-2 rounded-full font-medium transition-colors shadow-sm">Get Updates</a>
                </div>
            </div>
        </div>
    </nav>
    <main class="py-32 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 class="text-4xl font-bold mb-4">${title}</h1>
        <img src="https://logo.clearbit.com/pictory.ai?size=128" alt="Pictory AI Logo" class="mb-8 rounded-xl shadow-sm">
        <div class="prose prose-lg max-w-none">
${bodyHtml}
        </div>
    </main>
</body>
</html>`;

fs.writeFileSync('blog/pictory-ai-2026.html', template);
console.log('done');
