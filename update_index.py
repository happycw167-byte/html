import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Reference layout (col-md-6 to col-md-4)
start_idx = html.find('<!-- 3. 자료실 (Reference) -->')
if start_idx != -1:
    end_idx = html.find('<!-- 4. 고객지원 (Customer Support) -->', start_idx)
    reference_html = html[start_idx:end_idx]
    new_reference_html = reference_html.replace('col-md-6 mb-4', 'col-md-4 mb-4')
    html = html.replace(reference_html, new_reference_html)

# 2. Update Nav "고객지원" -> "연락처 및 오시는 길"
html = html.replace('<a href="#support" class="nav-link">고객지원</a>', '<a href="#support" class="nav-link">연락처 및 오시는 길</a>')

# 3. Update Section Title
html = html.replace('<h2 class="section-title">고객지원</h2>', '<h2 class="section-title">연락처 및 오시는 길</h2>')

# 4. Remove "자료실 & 공지사항" container
bad_block = """                    <div class="mt-4 p-4 bg-light" style="border-radius: 8px; padding: 25px;">
                        <h4 class="mb-3">자료실 & 공지사항</h4>
                        <p class="text-muted mb-3">제품 카탈로그, 도면, 인증서 사본 등 다양한 자료를 확인하실 수 있습니다.</p>
                        
                    </div>"""

# Sometimes there are trailing whitespaces, so regex is better
html = re.sub(r'<div class="mt-4 p-4 bg-light" style="border-radius: 8px; padding: 25px;">\s*<h4 class="mb-3">자료실 & 공지사항</h4>\s*<p class="text-muted mb-3">제품 카탈로그, 도면, 인증서 사본 등 다양한 자료를 확인하실 수 있습니다\.</p>\s*</div>', '', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
