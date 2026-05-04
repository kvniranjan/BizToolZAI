const fs = require('fs');

const htmlPath = 'blog/index.html';
let html = fs.readFileSync(htmlPath, 'utf8');

const injectionPoint = 'id="toolsGrid">';
const newCard = `
            <a href="munch-2026-05-04.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-bold text-primary uppercase tracking-wider">Video Creators</span>
                    <img src="https://logo.clearbit.com/getmunch.com?size=64" onerror="this.style.display='none'" class="w-8 h-8 rounded-md shadow-sm border border-border object-cover" alt="Munch AI Logo">
                </div>
                <h3 class="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">Munch AI Review 2026: Automate Your Video Editing Like a Pro</h3>
                <p class="text-muted-foreground text-sm mb-6 flex-grow">Discover how Munch AI revolutionizes video editing with customizable templates and intuitive tools.</p>
                <div class="flex justify-between items-center text-sm font-semibold text-secondary pt-4 border-t border-border">
                    <span>📖 3 min read</span>
                    <span>🚀 New</span>
                </div>
            </a>`;

if (!html.includes('munch-2026-05-04.html')) {
    html = html.replace(injectionPoint, injectionPoint + newCard);
    fs.writeFileSync(htmlPath, html);
    console.log('Updated blog/index.html');
} else {
    console.log('Already updated blog/index.html');
}
