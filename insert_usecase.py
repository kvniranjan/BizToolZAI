with open("use-cases/index.html", "r") as f:
    lines = f.readlines()

new_card = """    <a href="/use-cases/ai-for-social-media.html" class="bg-card border border-border p-8 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col items-center text-center">
        <div class="text-4xl mb-4">📱</div>
        <h3 class="text-2xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">AI for Social Media</h3>
        <p class="text-muted-foreground">Automate your social media presence with AI-generated posts, graphics, and smart scheduling.</p>
    </a>
"""

for i, line in enumerate(lines):
    if '<div class="grid grid-cols-1 md:grid-cols-2 gap-8">' in line:
        lines.insert(i + 1, new_card)
        break

with open("use-cases/index.html", "w") as f:
    f.writelines(lines)
