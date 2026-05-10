const fs = require('fs');

const date = '2026-05-10';
const toolName = 'Pollo AI';
const mdFile = 'content/Pollo_AI_2026-05-10.md';
const slug = 'pollo-ai';
const category = 'Video Creators';
const logoUrl = 'https://logo.clearbit.com/pollo.ai?size=64';

// 1. Read Markdown
const mdContent = fs.readFileSync(mdFile, 'utf8');

// Simple Markdown to HTML for the blog body (very basic, assuming just Title, Meta, and Review Body)
const reviewMatch = mdContent.match(/\*\*Review Body:\*\*\n([\s\S]+?)\n\n## Social/);
const reviewBody = reviewMatch ? reviewMatch[1].trim() : "Discover how Pollo AI is changing the video creation game.";

const titleMatch = mdContent.match(/\*\*Title:\*\*\n?(.*)/);
const title = titleMatch ? titleMatch[1].trim() : `${toolName} Review: The Ultimate AI Video Generator?`;

const blogHtml = `<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title} — BizToolz AI</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = { theme: { extend: { colors: { primary: '#0369A1' } } } }
    </script>
</head>
<body class="antialiased font-sans bg-[#F8FAFC] text-[#020617]">
    <main class="py-16 max-w-3xl mx-auto px-4">
        <img src="${logoUrl}" alt="${toolName} Logo" class="w-16 h-16 rounded-xl shadow-sm border mb-6" onerror="this.style.display='none'">
        <h1 class="text-4xl font-extrabold mb-8">${title}</h1>
        <div class="prose prose-lg">
            <p>${reviewBody}</p>
        </div>
    </main>
</body>
</html>`;

fs.writeFileSync(`blog/${slug}.html`, blogHtml);

// 2. Update blog/index.html
const blogIndex = fs.readFileSync('blog/index.html', 'utf8');
const cardHtml = `
            <a href="${slug}.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-bold text-primary uppercase tracking-wider">${category}</span>
                    <img src="${logoUrl}" onerror="this.style.display='none'" class="w-8 h-8 rounded-md shadow-sm border border-border object-cover" alt="${toolName} Logo">
                </div>
                <h3 class="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">${title}</h3>
                <p class="text-muted-foreground text-sm mb-6 flex-grow">${reviewBody.substring(0, 100)}...</p>
                <div class="flex justify-between items-center text-sm font-semibold text-secondary pt-4 border-t border-border">
                    <span>📖 3 min read</span>
                    <span>🚀 New</span>
                </div>
            </a>
`;
// insert right after toolsGrid opening
const updatedBlogIndex = blogIndex.replace('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">', '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">\n' + cardHtml);
fs.writeFileSync('blog/index.html', updatedBlogIndex);

// 3. Update use-cases/ai-for-video-creators.html
try {
    const hubIndex = fs.readFileSync('use-cases/ai-for-video-creators.html', 'utf8');
    const updatedHubIndex = hubIndex.replace('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">', '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">\n' + cardHtml.replace(`href="${slug}.html"`, `href="../blog/${slug}.html"`));
    fs.writeFileSync('use-cases/ai-for-video-creators.html', updatedHubIndex);
} catch (e) {
    console.log("Could not update hub:", e.message);
}

// 4. Update content_approval.csv
const csv = fs.readFileSync('content_approval.csv', 'utf8');
const updatedCsv = csv.replace('2026-05-10,Pollo AI,content/Pollo_AI_2026-05-10.md,Auto-Queue', '2026-05-10,Pollo AI,content/Pollo_AI_2026-05-10.md,Published');
fs.writeFileSync('content_approval.csv', updatedCsv);

console.log("Done");
