import re

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Remove ' hidden-equipment'
html = html.replace(' hidden-equipment', '')

# Remove the toggle button
button_pattern = r'<div class="text-center mt-4"><button id="btn-toggle-equipment"[^>]*>더보기 \(▼\)</button></div>'
html = re.sub(button_pattern, '', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

# 2. Clean main.js (Optional but good)
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

js_block = """
    // 장비 및 시설 더보기/접기 토글
    const btnToggleEq = document.getElementById('btn-toggle-equipment');
    if (btnToggleEq) {
        btnToggleEq.addEventListener('click', function() {
            const hiddenItems = document.querySelectorAll('.hidden-equipment');
            const isHidden = hiddenItems[0].style.display !== 'block';

            if (isHidden) {
                // 더보기
                hiddenItems.forEach(item => item.style.display = 'block');
                btnToggleEq.innerHTML = '접기 (▲)';
            } else {
                // 접기
                hiddenItems.forEach(item => item.style.display = '');
                btnToggleEq.innerHTML = '더보기 (▼)';
                
                // 접을 때 섹션 위로 스크롤 (선택적)
                const eqSection = document.getElementById('equipment');
                if (eqSection) {
                    eqSection.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    }
"""
js = js.replace(js_block, '')

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)

# 3. Clean style.css
with open("style.css", "r", encoding="utf-8") as f:
    css = f.read()

css_block = """
/* 장비 및 시설 숨김 처리 */
.hidden-equipment {
    display: none !important;
}
"""
css = css.replace(css_block, '')

with open("style.css", "w", encoding="utf-8") as f:
    f.write(css)

print("Rollback completed.")
