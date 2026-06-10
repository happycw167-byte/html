import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Targets to enlarge
targets = [
    '<h3 class="mb-3">기업 개요</h3>',
    '<h3 class="mb-3">조직도</h3>',
    '<h3 class="mb-4 text-center">카드뉴스</h3>',
    '<h3 class="mb-4 text-center"><i class="ph-fill ph-clock-counter-clockwise"></i> 회사연혁</h3>',
    '<h3 class="mb-4 text-center"><i class="ph-fill ph-chart-line-up"></i> 주요사업 실적</h3>',
    '<h3 class="mb-4">인증 및 수상</h3>'
]

replacement_style = ' style="font-size: 1.9rem; font-weight: 700;"'

for t in targets:
    # insert style into the h3 tag
    new_t = t.replace('<h3 ', f'<h3{replacement_style} ')
    html = html.replace(t, new_t)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Title sizes updated.")
