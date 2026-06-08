import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# CSS string to append
css_addition = """
/* Checkerboard Grid for Reference */
.checkerboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
}
.checkerboard-item {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-radius: 12px;
    overflow: hidden;
}
.checkerboard-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
}
"""

with open("style.css", "a", encoding="utf-8") as f:
    f.write(css_addition)

# Find reference section and replace it
start_idx = html.find('<!-- 3. 자료실 (Reference) -->')
if start_idx != -1:
    end_idx = html.find('<!-- 4. 고객지원 (Customer Support) -->', start_idx)
    if end_idx == -1:
        end_idx = html.find('<!-- 5. 문의하기 (Inquiry) -->', start_idx) # in case it changed
    ref_html = html[start_idx:end_idx]

    # Replace <div class="row"> with <div class="checkerboard-grid">
    # Replace col-md-6 mb-4 and inner card structure
    
    # We will use regex to find each card and transform it
    pattern = r'<div class="col-md-6 mb-4">\s*<a href="([^"]+)" onclick="([^"]+)" class="card shadow-sm text-decoration-none">\s*<div class="card-body d-flex align-items-center">\s*<i class="[^"]+" style="[^"]+"></i>\s*<div>\s*<h5 class="card-title text-dark mb-1"[^>]*>([^<]+)</h5>\s*<small class="text-muted">([^<]+)</small>\s*</div>\s*</div>\s*</a>\s*</div>'
    
    def replace_card(m):
        href = m.group(1)
        onclick = m.group(2)
        title = m.group(3)
        return f"""<a href="{href}" onclick="{onclick}" class="card shadow-sm text-decoration-none checkerboard-item">
                            <div class="card-body text-center d-flex flex-column justify-content-center align-items-center" style="height: 220px; padding: 30px;">
                                <i class="ph-fill ph-file-pdf text-danger mb-3" style="font-size: 4rem;"></i>
                                <h5 class="card-title text-dark mb-2" style="font-weight: 600;">{title}</h5>
                                <small class="text-muted">클릭하여 열람 및 다운로드</small>
                            </div>
                        </a>"""

    new_ref_html = re.sub(pattern, replace_card, ref_html)
    
    # Replace the container <div class="row"> to <div class="checkerboard-grid">
    new_ref_html = new_ref_html.replace('<div class="row">', '<div class="checkerboard-grid">')
    # Since we removed the wrapping col-md-6 divs in regex, the new structure directly puts <a> inside checkerboard-grid.
    # Wait, the closing </div> of <div class="row"> needs to be matched, but we just replaced the opening tag. The closing tag is still </div> which is fine for checkerboard-grid.
    
    html = html.replace(ref_html, new_ref_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Reference section updated to checkerboard format.")
