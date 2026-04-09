const fs = require('fs');
const { execSync } = require('child_process');

const csvPath = 'content_approval.csv';
const csv = fs.readFileSync(csvPath, 'utf8').trim().split('\n');
let lastRow = csv[csv.length - 1];

if (lastRow.includes('Reject') || lastRow.includes('Stop')) {
    console.log('Skipping due to status Reject/Stop.');
    process.exit(0);
}

const mdPath = 'content/HeyGen_2026-04-07.md';
const mdContent = fs.readFileSync(mdPath, 'utf8');

const title = "HeyGen Review 2026: The Best AI Video Generator?";
const meta = "Discover how HeyGen is transforming video creation with AI avatars and voice cloning. Read our complete review and find out if it's worth it in 2026.";

let bodyText = mdContent.split('## Review Body')[1].split('---')[0].trim();
let htmlBody = `<p>${bodyText.replace(/\n\n/g, '</p><p class="mt-4">')}</p>`;

const htmlDoc = `<!DOCTYPE html>
<html lang="en">
<head>
    <title>${title}</title>
    <meta name="description" content="${meta}">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #F8FAFC; color: #020617; font-family: 'Plus Jakarta Sans', sans-serif; }
    </style>
</head>
<body class="bg-gray-50 text-gray-900 font-sans p-8">
    <nav class="max-w-3xl mx-auto mb-8 flex items-center gap-4">
        <a href="/" class="text-blue-600 font-bold">&larr; Back to Home</a>
        <a href="/blog/" class="text-blue-600 font-bold">&larr; Back to Blog</a>
    </nav>
    <div class="max-w-3xl mx-auto bg-white p-8 rounded-2xl shadow">
        <div class="flex items-center gap-4 mb-6">
            <img src="https://logo.clearbit.com/heygen.com?size=64" onerror="this.style.display='none'" class="w-16 h-16 rounded-md shadow-sm border border-gray-200 object-cover" alt="HeyGen Logo">
            <h1 class="text-4xl font-bold">${title}</h1>
        </div>
        <div class="prose lg:prose-xl">
            ${htmlBody}
        </div>
    </div>
</body>
</html>`;

fs.writeFileSync('blog/heygen.html', htmlDoc);

// Update blog/index.html
const blogIndex = fs.readFileSync('blog/index.html', 'utf8');
const blogCard = `
            <a href="heygen.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-bold text-primary uppercase tracking-wider">Video Marketing</span>
                    <img src="https://logo.clearbit.com/heygen.com?size=64" onerror="this.style.display='none'" class="w-8 h-8 rounded-md shadow-sm border border-border object-cover" alt="HeyGen Logo">
                </div>
                <h3 class="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">${title}</h3>
                <p class="text-muted-foreground text-sm mb-6 flex-grow">${meta}</p>
                <div class="flex justify-between items-center text-sm font-semibold text-secondary pt-4 border-t border-border">
                    <span>📖 5 min read</span>
                    <span>🚀 New</span>
                </div>
            </a>`;
const newBlogIndex = blogIndex.replace('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">', '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">\n' + blogCard);
fs.writeFileSync('blog/index.html', newBlogIndex);

// Update use-cases/ai-for-video-creators.html
const useCaseFile = 'use-cases/ai-for-video-creators.html';
const useCaseHtml = fs.readFileSync(useCaseFile, 'utf8');
const useCaseCard = `
            <a href="/blog/heygen.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-xs font-bold text-primary uppercase tracking-wider">Video Marketing</span>
                    <img src="https://logo.clearbit.com/heygen.com?size=64" onerror="this.style.display='none'" class="w-10 h-10 rounded-lg shadow-sm border border-border object-cover" alt="HeyGen Logo">
                </div>
                <h3 class="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">${title}</h3>
                <p class="text-muted-foreground text-sm mb-6 flex-grow">${meta}</p>
                <div class="flex justify-between items-center text-sm font-semibold text-primary pt-4 border-t border-border">
                    <span>Read Breakdown &rarr;</span>
                </div>
            </a>`;
const newUseCaseHtml = useCaseHtml.replace('<div class="grid grid-cols-1 md:grid-cols-2 gap-8">', '<div class="grid grid-cols-1 md:grid-cols-2 gap-8">\n' + useCaseCard);
fs.writeFileSync(useCaseFile, newUseCaseHtml);

// Update CSV
csv[csv.length - 1] = lastRow.replace('Auto-Queue', 'Published');
fs.writeFileSync(csvPath, csv.join('\n') + '\n');

// Git
try {
    execSync('git add . && git commit -m "Publish HeyGen + Update Hubs" && git push origin main', { stdio: 'inherit' });
} catch (e) {
    console.log('Git failed or nothing to commit.');
}
