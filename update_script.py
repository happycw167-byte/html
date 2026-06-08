import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Navigation '연구개발' -> '자료실'
html = html.replace('<a href="#rnd" class="nav-link">연구개발</a>', '<a href="#reference" class="nav-link">자료실</a>')

# 2. Delete "자료실&공지사항" under "고객지원"
start_str = '<div style="display: flex; gap: 10px;">'
end_str = '                            <a href="#" class="btn btn-outline btn-sm" style="border-color: var(--primary-blue); color: var(--primary-blue);">사내 공지사항</a>\n                        </div>'
# Try to find this exact block to remove. Since there might be formatting diffs, I will use regex.
pattern = r'<div style="display: flex; gap: 10px;">\s*<a href="javascript:void\(0\)" id="btn-reference".*?</div>'
html = re.sub(pattern, '', html, flags=re.DOTALL)

# 3. Add 16 items to Major Achievements
items = [
    "김화하수처리구역(와수3처리분구) 하수관거정비사업 수중볼텍스펌프 (철원군상하수도사업소)",
    "농업용수(양덕원리 취수펌프) 배수관로 설치공사 진공펌프 (홍천군)",
    "용산정수장 샘플링펌프 (춘천시상하수도사업본부)",
    "근화동 유수지 지배수펌프 증설공사 수중펌프 (춘천시상하수도사업본부)",
    "본관기계실 노후펌프 교체공사 (강원도인재개발원)",
    "읍상빗물펌프장 펌프 수리수선 (삼척시하수도사업소)",
    "만경보 수중펌프 교체공사 관급자재(수중펌프) 구매 (철원군농업기술센터)",
    "홍천종합운동장 수영장 열교환기 펌프 및 인버터 교체 (홍천군시설관리사업소)",
    "홍천문화예술회관 외 1개소 저수조 배수펌프 교체공사 (홍천군시설관리사업소)",
    "상수도시설(가압장) 확충공사 관급자재(부스터펌프) 구매 (춘천시상하수도사업본부)",
    "북방배수지 송수펌프 교체 (홍천군)",
    "하수도시설 보수 및 개선공사(지방하천-홍천강지구) 수중펌프 (홍천군)",
    "강현가압장 가압시설 증설공사 관급자재(부스터펌프) (양양군상하수도사업소)",
    "평창군 대화면 하수관로 정비사업 관급자재(수중볼텍스펌프) (평창군상하수도사업소)",
    "평창군 진부면 하수관로 정비사업 관급자재(수중볼텍스펌프) (평창군상하수도사업소)",
    "철원군 화지리(2,3처리분구) 하수관거정비사업 수중볼텍스펌프 (철원군상하수도사업소)"
]

achievements_html = '<div class="timeline">\n'
for i, item in enumerate(items):
    achievements_html += f"""                                    <div class="timeline-item">
                                        <div class="timeline-year">2019</div>
                                        <div class="timeline-content">{item}</div>
                                    </div>\n"""
achievements_html += '                                </div>'

# find the existing timeline block for achievements
start_ach = html.find('<!-- 주요사업 실적 -->')
if start_ach != -1:
    timeline_start = html.find('<div class="timeline">', start_ach)
    timeline_end = html.find('</div>\n                            </div>\n                        </div>\n                    </div>', timeline_start)
    if timeline_start != -1 and timeline_end != -1:
        # Actually timeline_end is just '</div>' for the timeline container.
        end_idx = html.find('</div>', html.find('</div>', html.find('</div>', timeline_start) + 1) + 1) # wait, better to use regex
        # let's just use regex for the timeline block inside 주요사업 실적
        html = re.sub(r'(<!-- 주요사업 실적 -->.*?<h3.*?>.*?</h3>\s*)<div class="timeline">.*?</div>\s*</div>\s*</div>\s*</div>',
                      r'\1' + achievements_html + '\n                            </div>\n                        </div>\n                    </div>', html, flags=re.DOTALL)


# 4. Make "장비 및 시설" images clickable modal
# We will change `<div class="equipment-img-wrapper">` to `<div class="equipment-img-wrapper" onclick="openCertModal('factory_img_X.jpeg')" style="cursor:pointer;">`
def repl_equipment(m):
    img_tag = m.group(1)
    # extract src
    src_match = re.search(r'src="([^"]+)"', img_tag)
    src = src_match.group(1) if src_match else ""
    return f'<div class="equipment-img-wrapper" onclick="openCertModal(\'{src}\')" style="cursor:pointer;">\n{img_tag}'

html = re.sub(r'<div class="equipment-img-wrapper">\s*(<img[^>]+>)', repl_equipment, html)


# 5. Replace '연구개발 (R&D)' section with '자료실' (Reference)
reference_section_html = """
    <!-- 3. 자료실 (Reference) -->
    <section id="reference" class="reference section bg-light">
        <div class="container">
            <div class="section-header text-center fade-up">
                <h2 class="section-title">자료실</h2>
                <p>Reference</p>
                <p class="mt-3 text-muted">펌프 유지관리지침서 등 각종 자료를 다운로드 하실 수 있습니다.</p>
            </div>
            <div class="reference-list mt-5 fade-up">
                <div class="row">
                    <div class="col-md-6 mb-4">
                        <a href="./부스터펌프 유지관리지침서.pdf" target="_blank" class="card shadow-sm text-decoration-none">
                            <div class="card-body d-flex align-items-center">
                                <i class="ph-fill ph-file-pdf text-danger" style="font-size: 2.5rem; margin-right: 15px;"></i>
                                <div>
                                    <h5 class="card-title text-dark mb-1" style="font-weight: 600;">부스터펌프 유지관리지침서</h5>
                                    <small class="text-muted">PDF 파일 열람 및 다운로드</small>
                                </div>
                            </div>
                        </a>
                    </div>
                    <div class="col-md-6 mb-4">
                        <a href="./수중펌프 유지관리지침서.pdf" target="_blank" class="card shadow-sm text-decoration-none">
                            <div class="card-body d-flex align-items-center">
                                <i class="ph-fill ph-file-pdf text-danger" style="font-size: 2.5rem; margin-right: 15px;"></i>
                                <div>
                                    <h5 class="card-title text-dark mb-1" style="font-weight: 600;">수중펌프 유지관리지침서</h5>
                                    <small class="text-muted">PDF 파일 열람 및 다운로드</small>
                                </div>
                            </div>
                        </a>
                    </div>
                    <div class="col-md-6 mb-4">
                        <a href="./슬러지펌프 유지관리지침서.pdf" target="_blank" class="card shadow-sm text-decoration-none">
                            <div class="card-body d-flex align-items-center">
                                <i class="ph-fill ph-file-pdf text-danger" style="font-size: 2.5rem; margin-right: 15px;"></i>
                                <div>
                                    <h5 class="card-title text-dark mb-1" style="font-weight: 600;">슬러지펌프 유지관리지침서</h5>
                                    <small class="text-muted">PDF 파일 열람 및 다운로드</small>
                                </div>
                            </div>
                        </a>
                    </div>
                    <div class="col-md-6 mb-4">
                        <a href="./일축나사식 모노펌프 유지관리지침서.pdf" target="_blank" class="card shadow-sm text-decoration-none">
                            <div class="card-body d-flex align-items-center">
                                <i class="ph-fill ph-file-pdf text-danger" style="font-size: 2.5rem; margin-right: 15px;"></i>
                                <div>
                                    <h5 class="card-title text-dark mb-1" style="font-weight: 600;">일축나사식 모노펌프 유지관리지침서</h5>
                                    <small class="text-muted">PDF 파일 열람 및 다운로드</small>
                                </div>
                            </div>
                        </a>
                    </div>
                    <div class="col-md-6 mb-4">
                        <a href="./정량펌프 유지관리지침서.pdf" target="_blank" class="card shadow-sm text-decoration-none">
                            <div class="card-body d-flex align-items-center">
                                <i class="ph-fill ph-file-pdf text-danger" style="font-size: 2.5rem; margin-right: 15px;"></i>
                                <div>
                                    <h5 class="card-title text-dark mb-1" style="font-weight: 600;">정량펌프 유지관리지침서</h5>
                                    <small class="text-muted">PDF 파일 열람 및 다운로드</small>
                                </div>
                            </div>
                        </a>
                    </div>
                    <div class="col-md-6 mb-4">
                        <a href="./편흡입볼류트펌프 유지관리지침서.pdf" target="_blank" class="card shadow-sm text-decoration-none">
                            <div class="card-body d-flex align-items-center">
                                <i class="ph-fill ph-file-pdf text-danger" style="font-size: 2.5rem; margin-right: 15px;"></i>
                                <div>
                                    <h5 class="card-title text-dark mb-1" style="font-weight: 600;">편흡입볼류트펌프 유지관리지침서</h5>
                                    <small class="text-muted">PDF 파일 열람 및 다운로드</small>
                                </div>
                            </div>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </section>
"""

# Replace the R&D section with Reference section
html = re.sub(r'<!-- 3\. 연구개발 \(R&D\) -->.*?</section>', reference_section_html, html, flags=re.DOTALL)


with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
