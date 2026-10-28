import re

with open('c:/Users/DELL/Downloads/ai-recruiter-all-phases-sqlite/ai-recruiter/frontend-html/js/portfolio-themes.js', 'r', encoding='utf-8') as f:
    content = f.read()

layout_names = [
    "renderNovaEditorialLayout",
    "renderModernBentoLayout",
    "renderDeveloperIdeLayout",
    "renderCreativeStudioLayout",
    "renderCorporateExecutiveLayout",
    "renderAiTechHudLayout",
    "renderMinimalEditorialLayout",
    "renderDarkLuxuryLayout",
    "renderElegantGazetteLayout",
    "renderNotionDocLayout",
    "renderTimelineJourneyLayout",
    "renderDashboardCockpitLayout",
    "renderSplitScreenLayout"
]

for name in layout_names:
    m = re.search(r'function\s+' + name + r'\s*\([^)]*\)\s*\{', content)
    if not m:
        continue
    start = m.start()
    # find next function or end
    next_m = re.search(r'\n  function render[A-Z]', content[start+20:])
    end = start + 20 + next_m.start() if next_m else len(content)
    code = content[start:end]
    
    print(f"\n==================== {name} ====================")
    # Check for about
    has_about_id = 'id="section-about"' in code or "id='section-about'" in code
    # Check for education
    has_edu_id = 'id="section-education"' in code or "id='section-education'" in code
    # Check for certs
    has_certs_id = 'id="section-certifications"' in code or "id='section-certifications'" in code
    # Check for achievements
    has_ach_id = 'id="section-achievements"' in code or "id='section-achievements'" in code
    
    print(f"About ID: {has_about_id} | Edu ID: {has_edu_id} | Certs ID: {has_certs_id} | Ach ID: {has_ach_id}")
    
    # Check if education or certs are rendered
    edu_mention = 'education' in code
    certs_mention = 'cert' in code
    ach_mention = 'achieve' in code or 'Testimonials' in code
    print(f"Code mentions: Edu={edu_mention}, Certs={certs_mention}, Ach={ach_mention}")
