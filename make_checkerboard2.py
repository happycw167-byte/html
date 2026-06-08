import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

start_idx = html.find('<!-- 3. 자료실 (Reference) -->')
if start_idx != -1:
    end_idx = html.find('<!-- 4. 고객지원 (Customer Support) -->', start_idx)
    if end_idx == -1:
        end_idx = html.find('<!-- 5. 문의하기 (Inquiry) -->', start_idx)
    ref_html = html[start_idx:end_idx]

    # The card structure we want to match:
    # <div class="col-md-4 mb-4">
    #     <a href="javascript:void(0)" onclick="openPdfModal('./부스터펌프 유지관리지침서.pdf')" class="card shadow-sm text-decoration-none">
    #         <div class="card-body d-flex align-items-center">
    #             <i class="ph-fill ph-file-pdf text-danger" style="font-size: 2.5rem; margin-right: 15px;"></i>
    #             <div>
    #                 <h5 class="card-title text-dark mb-1" style="font-weight: 600;">부스터펌프 유지관리지침서</h5>
    #                 <small class="text-muted">PDF 파일 열람 및 다운로드</small>
    #             </div>
    #         </div>
    #     </a>
    # </div>
    
    # We will use regex to find each card and transform it
    pattern = r'<div class="col-md-4 mb-4">\s*<a href="([^"]+)" onclick="([^"]+)" class="card shadow-sm text-decoration-none">\s*<div class="card-body d-flex align-items-center">\s*<i class="[^"]+" style="[^"]+"></i>\s*<div>\s*<h5 class="card-title text-dark mb-1"[^>]*>([^<]+)</h5>\s*<small class="text-muted">([^<]+)</small>\s*</div>\s*</div>\s*</a>\s*</div>'
    
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
    
    html = html.replace(ref_html, new_ref_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Reference section updated to checkerboard format successfully.")
