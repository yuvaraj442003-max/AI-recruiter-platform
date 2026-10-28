import re

with open('c:/Users/DELL/Downloads/ai-recruiter-all-phases-sqlite/ai-recruiter/frontend-html/js/portfolio-themes.js', 'r', encoding='utf-8') as f:
    content = f.read()

layout_matches = list(re.finditer(r'function (render[A-Za-z0-9]+Layout)\s*\(data,\s*activeSections', content))

target_sections = ['about', 'skills', 'experience', 'projects', 'education', 'certifications', 'achievements', 'contact']

for i, m in enumerate(layout_matches):
    start = m.start()
    end = layout_matches[i+1].start() if i+1 < len(layout_matches) else len(content)
    layout_name = m.group(1)
    layout_code = content[start:end]
    
    missing = []
    found = []
    for s in target_sections:
        # Check if id="section-{s}" exists
        if f'id="section-{s}"' in layout_code or f"id='section-{s}'" in layout_code:
            found.append(s)
        else:
            missing.append(s)
            
    print(f"\n{layout_name}:")
    print(f"  FOUND IDs: {found}")
    print(f"  MISSING IDs: {missing}")
