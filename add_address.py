import re
import random

# Generate random phone numbers
def gen_phone():
    return f"033-264-{random.randint(1000, 9999)}"

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

address_modal = f"""
    <!-- 사내 주소록 모달 -->
    <div id="address-modal-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:2100; align-items:center; justify-content:center;">
        <div id="address-modal" style="background:#fff; width:90%; max-width:600px; border-radius:12px; overflow:hidden; box-shadow:0 15px 30px rgba(0,0,0,0.2);">
            <div style="background:var(--primary-blue); color:#fff; padding:15px 20px; display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; font-size:1.2rem; color:#fff;"><i class="ph-fill ph-address-book"></i> 사내 주소록</h4>
                <button onclick="closeAddressBook()" style="background:none; border:none; font-size:1.5rem; cursor:pointer; color:#fff;">&times;</button>
            </div>
            <div style="padding: 20px; max-height: 400px; overflow-y: auto;">
                <table class="table table-hover text-center" style="margin:0;">
                    <thead style="background:#f8f9fa;">
                        <tr>
                            <th>이름</th>
                            <th>부서</th>
                            <th>직급</th>
                            <th>전화번호</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>조세연</td><td>임원진</td><td>대표이사</td><td>033-264-9243</td></tr>
                        <tr><td>정충구</td><td>생산부</td><td>부장</td><td>{gen_phone()}</td></tr>
                        <tr><td>조태연</td><td>생산부</td><td>부장</td><td>{gen_phone()}</td></tr>
                        <tr><td>김진수</td><td>생산부</td><td>과장</td><td>{gen_phone()}</td></tr>
                        <tr><td>이원석</td><td>관리부</td><td>이사</td><td>{gen_phone()}</td></tr>
                        <tr><td>김홍인</td><td>관리부</td><td>실장</td><td>{gen_phone()}</td></tr>
                        <tr><td>정영호</td><td>품질보증부</td><td>사원</td><td>{gen_phone()}</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
"""

# Insert modal right before </body>
html = html.replace('</body>', address_modal + '\n</body>')

# Change onclick
old_onclick = "onclick=\"alert('사내 주소록 기능은 준비 중입니다.')\""
new_onclick = "onclick=\"openAddressBook()\""
html = html.replace(old_onclick, new_onclick)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

# Update main.js
js_addition = """
function openAddressBook() {
    document.getElementById('address-modal-overlay').style.display = 'flex';
}
function closeAddressBook() {
    document.getElementById('address-modal-overlay').style.display = 'none';
}
"""

with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Add new functions at the end
js += js_addition

# Also update the window click listener
if "const addressOverlay = document.getElementById('address-modal-overlay');" not in js:
    # Need to inject inside the existing window.addEventListener('click'...)
    # The existing block ends with closeInternalModal(); } });
    replace_target = "if (event.target === internalOverlay) {\n        closeInternalModal();\n    }"
    replacement = replace_target + "\n    const addressOverlay = document.getElementById('address-modal-overlay');\n    if (event.target === addressOverlay) {\n        closeAddressBook();\n    }"
    js = js.replace(replace_target, replacement)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Address book added.")
