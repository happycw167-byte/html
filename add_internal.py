import re

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add Nav link
nav_str = '<a href="#support" class="nav-link">연락처 및 오시는 길</a>'
new_nav_str = nav_str + '\n                <a href="javascript:void(0)" onclick="openPwModal()" class="nav-link" style="color:var(--primary-blue); font-weight:bold;">사내 시스템</a>'
html = html.replace(nav_str, new_nav_str)

# Add Modals before </body>
modals_html = """
    <!-- 사내 시스템 패스워드 모달 -->
    <div id="pw-modal-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:2000; align-items:center; justify-content:center;">
        <div id="pw-modal" style="background:#fff; width:90%; max-width:400px; border-radius:12px; overflow:hidden; box-shadow:0 15px 30px rgba(0,0,0,0.2);">
            <div style="background:#f8f9fa; padding:15px 20px; border-bottom:1px solid #ddd; display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; font-size:1.2rem; color:var(--primary-blue);"><i class="ph-fill ph-lock-key"></i> 관리자 인증</h4>
                <button onclick="closePwModal()" style="background:none; border:none; font-size:1.5rem; cursor:pointer; color:#666;">&times;</button>
            </div>
            <div style="padding: 30px 20px; text-align: center;">
                <p style="margin-bottom: 20px; color: #555;">사내 시스템에 접근하려면 비밀번호를 입력해주세요.</p>
                <input type="password" id="system-pw-input" placeholder="비밀번호 입력" style="width:100%; padding:10px; margin-bottom:15px; border:1px solid #ccc; border-radius:6px; font-size:1rem;" onkeypress="if(event.key==='Enter') checkPassword()">
                <button onclick="checkPassword()" class="btn btn-primary" style="width:100%;">확인</button>
                <p id="pw-error-msg" style="color:red; margin-top:10px; display:none; font-size:0.9rem;">비밀번호가 일치하지 않습니다.</p>
            </div>
        </div>
    </div>

    <!-- 사내 시스템 메인 모달 -->
    <div id="internal-modal-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:2000; align-items:center; justify-content:center;">
        <div id="internal-modal" style="background:#fff; width:90%; max-width:600px; border-radius:12px; overflow:hidden; box-shadow:0 15px 30px rgba(0,0,0,0.2);">
            <div style="background:var(--primary-blue); color:#fff; padding:15px 20px; display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; font-size:1.2rem; color:#fff;"><i class="ph-fill ph-desktop"></i> 사내 시스템</h4>
                <button onclick="closeInternalModal()" style="background:none; border:none; font-size:1.5rem; cursor:pointer; color:#fff;">&times;</button>
            </div>
            <div style="padding: 30px 20px;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
                    <a href="javascript:void(0)" onclick="alert('사내 주소록 기능은 준비 중입니다.')" class="card text-center" style="text-decoration:none; padding:30px 15px; border:1px solid #eee; border-radius:8px; transition:all 0.3s ease; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                        <i class="ph-fill ph-address-book text-primary" style="font-size:3rem; margin-bottom:15px;"></i>
                        <h6 class="text-dark" style="margin:0; font-weight:600;">사내 주소록</h6>
                    </a>
                    <a href="javascript:void(0)" onclick="alert('NotebookLM 지침서 기능은 준비 중입니다.')" class="card text-center" style="text-decoration:none; padding:30px 15px; border:1px solid #eee; border-radius:8px; transition:all 0.3s ease; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                        <i class="ph-fill ph-book-open-text text-success" style="font-size:3rem; margin-bottom:15px;"></i>
                        <h6 class="text-dark" style="margin:0; font-weight:600;">NotebookLM<br>지침서</h6>
                    </a>
                    <a href="javascript:void(0)" onclick="alert('사내 공지사항 기능은 준비 중입니다.')" class="card text-center" style="text-decoration:none; padding:30px 15px; border:1px solid #eee; border-radius:8px; transition:all 0.3s ease; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                        <i class="ph-fill ph-megaphone text-warning" style="font-size:3rem; margin-bottom:15px;"></i>
                        <h6 class="text-dark" style="margin:0; font-weight:600;">사내 공지사항</h6>
                    </a>
                </div>
            </div>
        </div>
    </div>
"""

# add modals right before </body>
html = html.replace('</body>', modals_html + '\n</body>')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

# 2. Update main.js
js_addition = """
// 사내 시스템 패스워드 모달
function openPwModal() {
    document.getElementById('pw-modal-overlay').style.display = 'flex';
    document.getElementById('system-pw-input').value = '';
    document.getElementById('pw-error-msg').style.display = 'none';
    document.getElementById('system-pw-input').focus();
}

function closePwModal() {
    document.getElementById('pw-modal-overlay').style.display = 'none';
}

function checkPassword() {
    const pwInput = document.getElementById('system-pw-input').value;
    const errorMsg = document.getElementById('pw-error-msg');
    
    if (pwInput === 'ba12') {
        closePwModal();
        openInternalModal();
    } else {
        errorMsg.style.display = 'block';
    }
}

function openInternalModal() {
    document.getElementById('internal-modal-overlay').style.display = 'flex';
}

function closeInternalModal() {
    document.getElementById('internal-modal-overlay').style.display = 'none';
}

// 오버레이 클릭 시 닫기 기능 추가 (옵션)
window.addEventListener('click', function(event) {
    const pwOverlay = document.getElementById('pw-modal-overlay');
    const internalOverlay = document.getElementById('internal-modal-overlay');
    if (event.target === pwOverlay) {
        closePwModal();
    }
    if (event.target === internalOverlay) {
        closeInternalModal();
    }
});
"""

with open("main.js", "a", encoding="utf-8") as f:
    f.write(js_addition)

print("Internal System feature added.")
