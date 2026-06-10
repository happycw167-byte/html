import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fix overlap by adding padding-top to the equipment section
old_eq = '<section id="equipment" class="services section">'
new_eq = '<section id="equipment" class="services section" style="padding-top: 120px;">'
if old_eq in html:
    html = html.replace(old_eq, new_eq)

# 2. Add brochure to reference list
old_ref = """                    <a href="javascript:void(0)" onclick="openPdfModal('./일축나사식 모노펌프 유지관리지침서.pdf')" class="card shadow-sm text-decoration-none checkerboard-item">
                        <div class="card-body text-center d-flex flex-column justify-content-center align-items-center" style="height: 220px; padding: 30px;">
                            <i class="ph-fill ph-file-pdf text-danger mb-3" style="font-size: 4rem;"></i>
                            <h5 class="card-title text-dark mb-2" style="font-weight: 600;">일축나사식 모노펌프 유지관리지침서</h5>
                            <small class="text-muted">클릭하여 열람 및 다운로드</small>
                        </div>
                    </a>"""

new_ref = old_ref + """
                    <a href="brochure.png" target="_blank" download="비에이텍_브로슈어.png" class="card shadow-sm text-decoration-none checkerboard-item">
                        <div class="card-body text-center d-flex flex-column justify-content-center align-items-center" style="height: 220px; padding: 30px;">
                            <i class="ph-fill ph-file-image text-primary mb-3" style="font-size: 4rem;"></i>
                            <h5 class="card-title text-dark mb-2" style="font-weight: 600;">비에이텍(주) 브로슈어</h5>
                            <small class="text-muted">클릭하여 열람 및 다운로드</small>
                        </div>
                    </a>"""

if old_ref in html:
    html = html.replace(old_ref, new_ref)
else:
    print("Could not find reference to append brochure.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updates applied successfully.")
