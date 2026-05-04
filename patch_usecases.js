const fs = require('fs');

const htmlPath = 'use-cases/ai-for-video-creators.html';
let html = fs.readFileSync(htmlPath, 'utf8');

const injectionPoint = '<div class="grid grid-cols-1 md:grid-cols-2 gap-8">';
const newCard = `
            <a href="/blog/munch-2026-05-04.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full bg-white">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-bold text-primary text-blue-600 uppercase tracking-wider">Video Creators</span>
                    <img src="https://logo.clearbit.com/getmunch.com?size=64" onerror="this.style.display='none'" class="w-10 h-10 rounded-md border border-gray-100 object-cover" alt="Munch AI Logo">
                </div>
                <h3 class="text-xl font-bold text-foreground text-gray-900 mb-3 group-hover:text-blue-600 transition-colors">Munch AI Review 2026: Automate Your Video Editing Like a Pro</h3>
                <p class="text-muted-foreground text-gray-600 text-sm mb-6 flex-grow">Discover how Munch AI revolutionizes video editing with customizable templates and intuitive tools.</p>
                <div class="flex justify-between items-center text-sm font-semibold text-secondary pt-4 border-t border-border">
                    <span>Read Review &rarr;</span>
                </div>
            </a>`;

if (!html.includes('munch-2026-05-04.html')) {
    html = html.replace(injectionPoint, injectionPoint + newCard);
    fs.writeFileSync(htmlPath, html);
    console.log('Updated use-cases/ai-for-video-creators.html');
} else {
    console.log('Already updated use-cases/ai-for-video-creators.html');
}
