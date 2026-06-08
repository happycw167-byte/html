import re

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# We need to find the equipment section and add hidden-equipment to the 9th to 16th item.
start_idx = html.find('<!-- 2. 장비 및 시설 (Equipment) -->')
end_idx = html.find('<!-- 3. 자료실 (Reference) -->')

if start_idx != -1 and end_idx != -1:
    eq_html = html[start_idx:end_idx]
    
    # Find all equipment-item divs
    # We will split by <div class="equipment-item
    parts = eq_html.split('<div class="equipment-item')
    
    # parts[0] is the content before the first item
    # parts[1] to parts[16] are the 16 items. We need to add ' hidden-equipment' to parts 9 to 16.
    for i in range(9, len(parts)):
        # It usually starts with ' fade-up"' or ' fade-up" style=...'
        parts[i] = parts[i].replace(' fade-up"', ' fade-up hidden-equipment"', 1)
        
    new_eq_html = '<div class="equipment-item'.join(parts)
    
    # Add the toggle button after equipment-grid
    btn_html = '\n                <div class="text-center mt-4"><button id="btn-toggle-equipment" class="btn btn-outline btn-sm" style="border-color:var(--primary-blue); color:var(--primary-blue); padding: 8px 30px; font-weight: 600;">더보기 (▼)</button></div>\n'
    
    # Replace the closing </div> of equipment-grid with </div> + btn_html
    new_eq_html = new_eq_html.replace('                </div>\n            </div>\n        </div>\n    </section>', f'                </div>{btn_html}            </div>\n        </div>\n    </section>')
    
    html = html.replace(eq_html, new_eq_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

# 2. Update style.css
css_addition = """
/* 장비 및 시설 숨김 처리 */
.hidden-equipment {
    display: none !important;
}
"""
with open("style.css", "a", encoding="utf-8") as f:
    f.write(css_addition)

# 3. Update main.js
js_addition = """
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

with open("main.js", "a", encoding="utf-8") as f:
    f.write(js_addition)

print("Equipment toggle feature added successfully.")
