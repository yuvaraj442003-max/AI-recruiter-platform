import re

with open('c:/Users/DELL/Downloads/ai-recruiter-all-phases-sqlite/ai-recruiter/frontend-html/js/portfolio-themes.js', 'r', encoding='utf-8') as f:
    content = f.read()

layout_matches = list(re.finditer(r'function (render[A-Za-z0-9]+Layout)\s*\(data,\s*activeSections', content))
for i, m in enumerate(layout_matches):
    start = m.start()
    end = layout_matches[i+1].start() if i+1 < len(layout_matches) else len(content)
    layout_name = m.group(1)
    layout_code = content[start:end]
    
    # Find nav or header
    nav_match = re.search(r'(<header[\s\S]*?</header>|<nav[\s\S]*?</nav>|navLinks[\s\S]*?;)', layout_code)
    has_nav = "YES" if nav_match else "NO"
    print(f"{layout_name}: has navbar: {has_nav}")
    if nav_match:
        snippet = nav_match.group(0)[:150].replace('\n', ' ')
        print(f"   Snippet: {snippet}...")
