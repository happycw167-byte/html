import re

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Modify onclick for '사내 공지사항'
old_onclick = "onclick=\"alert('사내 공지사항 기능은 준비 중입니다.')\""
new_onclick = "onclick=\"openBoardList()\""
html = html.replace(old_onclick, new_onclick)

modals_html = """
    <!-- 게시판 목록 모달 -->
    <div id="board-list-modal-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:2200; align-items:center; justify-content:center;">
        <div id="board-list-modal" style="background:#fff; width:90%; max-width:800px; height:80vh; max-height:600px; border-radius:12px; overflow:hidden; box-shadow:0 15px 30px rgba(0,0,0,0.2); display:flex; flex-direction:column; position:relative;">
            <div style="background:var(--primary-blue); color:#fff; padding:15px 20px; display:flex; justify-content:space-between; align-items:center; flex-shrink:0;">
                <h4 style="margin:0; font-size:1.2rem; color:#fff;"><i class="ph-fill ph-megaphone"></i> 사내 공지사항</h4>
                <button onclick="closeBoardList()" style="background:none; border:none; font-size:1.5rem; cursor:pointer; color:#fff;">&times;</button>
            </div>
            <div style="padding: 20px; overflow-y: auto; flex-grow:1;">
                <table class="table table-hover text-center" style="margin:0;">
                    <thead style="background:#f8f9fa;">
                        <tr>
                            <th style="width:10%;">번호</th>
                            <th style="width:60%;">제목</th>
                            <th style="width:15%;">작성자</th>
                            <th style="width:15%;">작성일</th>
                        </tr>
                    </thead>
                    <tbody id="board-list-body">
                        <!-- JS will render rows here -->
                    </tbody>
                </table>
            </div>
            <!-- Floating + Button -->
            <button onclick="openBoardCreate()" class="fab-btn shadow-lg" title="글쓰기">
                <i class="ph-bold ph-plus"></i>
            </button>
        </div>
    </div>

    <!-- 게시물 작성 모달 -->
    <div id="board-create-modal-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:2300; align-items:center; justify-content:center;">
        <div id="board-create-modal" style="background:#fff; width:90%; max-width:600px; border-radius:12px; overflow:hidden; box-shadow:0 15px 30px rgba(0,0,0,0.2);">
            <div style="background:#f8f9fa; padding:15px 20px; border-bottom:1px solid #ddd; display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; font-size:1.2rem; color:var(--primary-blue);">공지사항 작성</h4>
                <button onclick="closeBoardCreate()" style="background:none; border:none; font-size:1.5rem; cursor:pointer; color:#666;">&times;</button>
            </div>
            <div style="padding: 20px;">
                <div class="form-group mb-3">
                    <label for="board-title-input" style="font-weight:600; margin-bottom:5px; display:block;">제목 <span class="text-danger">*</span></label>
                    <input type="text" id="board-title-input" class="form-control" placeholder="제목을 입력하세요">
                </div>
                <div class="form-group mb-3">
                    <label for="board-content-input" style="font-weight:600; margin-bottom:5px; display:block;">내용 <span class="text-danger">*</span></label>
                    <textarea id="board-content-input" class="form-control" rows="8" placeholder="내용을 입력하세요"></textarea>
                </div>
                <div class="form-group mb-4">
                    <label for="board-file-input" style="font-weight:600; margin-bottom:5px; display:block;">첨부파일</label>
                    <input type="file" id="board-file-input" class="form-control">
                </div>
                <div style="display:flex; justify-content:flex-end; gap:10px;">
                    <button onclick="closeBoardCreate()" class="btn btn-secondary">취소</button>
                    <button onclick="submitBoard()" class="btn btn-primary">게시하기</button>
                </div>
            </div>
        </div>
    </div>

    <!-- 게시물 상세 모달 -->
    <div id="board-detail-modal-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:2300; align-items:center; justify-content:center;">
        <div id="board-detail-modal" style="background:#fff; width:90%; max-width:600px; border-radius:12px; overflow:hidden; box-shadow:0 15px 30px rgba(0,0,0,0.2);">
            <div style="background:#f8f9fa; padding:15px 20px; border-bottom:1px solid #ddd; display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; font-size:1.2rem; color:var(--primary-blue);">공지사항</h4>
                <button onclick="closeBoardDetail()" style="background:none; border:none; font-size:1.5rem; cursor:pointer; color:#666;">&times;</button>
            </div>
            <div style="padding: 20px;">
                <h3 id="detail-title" style="margin-bottom:10px; font-size:1.4rem;"></h3>
                <div style="font-size:0.9rem; color:#666; margin-bottom:20px; padding-bottom:10px; border-bottom:1px solid #eee;">
                    작성자: <span id="detail-author"></span> &nbsp;|&nbsp; 작성일: <span id="detail-date"></span>
                </div>
                <div id="detail-content" style="min-height:200px; white-space:pre-wrap; line-height:1.6; margin-bottom:20px;"></div>
                
                <div id="detail-file-area" style="display:none; background:#f1f3f5; padding:10px 15px; border-radius:6px;">
                    <i class="ph-fill ph-paperclip"></i> 첨부파일: <span id="detail-file-name" style="font-weight:600; cursor:pointer; color:var(--primary-blue); text-decoration:underline;"></span>
                </div>
                
                <div style="text-align:center; margin-top:30px;">
                    <button onclick="closeBoardDetail()" class="btn btn-primary">목록으로</button>
                </div>
            </div>
        </div>
    </div>
"""

html = html.replace('</body>', modals_html + '\n</body>')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

# 2. Update style.css
css_addition = """
/* Board FAB Button */
.fab-btn {
    position: absolute;
    bottom: 30px;
    right: 30px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: var(--primary-blue);
    color: white;
    border: none;
    font-size: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: transform 0.2s, background-color 0.2s;
    z-index: 10;
}
.fab-btn:hover {
    transform: scale(1.1);
    background-color: #0d47a1;
}

.board-row {
    cursor: pointer;
    transition: background-color 0.2s;
}
.board-row:hover {
    background-color: #f1f3f5 !important;
}
"""
with open("style.css", "a", encoding="utf-8") as f:
    f.write(css_addition)

# 3. Update main.js
js_addition = """
// --- 사내 공지사항 게시판 로직 ---

let boardData = JSON.parse(localStorage.getItem('boardData')) || [
    {
        id: 1,
        title: "신규 사내 시스템 오픈 안내",
        content: "임직원 여러분,\\n금일부터 신규 사내 시스템이 오픈되었습니다.\\n게시판과 주소록 기능을 적극 활용해주시기 바랍니다.\\n\\n감사합니다.",
        author: "관리자",
        date: "2026-06-09",
        fileName: ""
    }
];

function renderBoard() {
    const tbody = document.getElementById('board-list-body');
    if(!tbody) return;
    
    tbody.innerHTML = '';
    
    // Sort by id descending (newest first)
    const sortedData = [...boardData].sort((a, b) => b.id - a.id);
    
    if(sortedData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="padding:30px; color:#999;">등록된 공지사항이 없습니다.</td></tr>';
        return;
    }
    
    sortedData.forEach(item => {
        const tr = document.createElement('tr');
        tr.className = 'board-row';
        tr.onclick = () => openBoardDetail(item.id);
        
        tr.innerHTML = `
            <td>${item.id}</td>
            <td style="text-align:left; padding-left:20px; font-weight:500;">${item.title} ${item.fileName ? '<i class="ph-fill ph-paperclip text-muted" style="font-size:0.9rem;"></i>' : ''}</td>
            <td>${item.author}</td>
            <td>${item.date}</td>
        `;
        tbody.appendChild(tr);
    });
}

function openBoardList() {
    renderBoard();
    document.getElementById('board-list-modal-overlay').style.display = 'flex';
}

function closeBoardList() {
    document.getElementById('board-list-modal-overlay').style.display = 'none';
}

function openBoardCreate() {
    document.getElementById('board-title-input').value = '';
    document.getElementById('board-content-input').value = '';
    document.getElementById('board-file-input').value = '';
    document.getElementById('board-create-modal-overlay').style.display = 'flex';
}

function closeBoardCreate() {
    document.getElementById('board-create-modal-overlay').style.display = 'none';
}

function submitBoard() {
    const title = document.getElementById('board-title-input').value.trim();
    const content = document.getElementById('board-content-input').value.trim();
    const fileInput = document.getElementById('board-file-input');
    
    if(!title || !content) {
        alert("제목과 내용을 모두 입력해주세요.");
        return;
    }
    
    let fileName = "";
    if(fileInput.files.length > 0) {
        fileName = fileInput.files[0].name;
    }
    
    const today = new Date();
    const dateStr = today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
    
    const newId = boardData.length > 0 ? Math.max(...boardData.map(d => d.id)) + 1 : 1;
    
    const newItem = {
        id: newId,
        title: title,
        content: content,
        author: "임직원",
        date: dateStr,
        fileName: fileName
    };
    
    boardData.push(newItem);
    localStorage.setItem('boardData', JSON.stringify(boardData));
    
    closeBoardCreate();
    renderBoard();
}

function openBoardDetail(id) {
    const item = boardData.find(d => d.id === id);
    if(!item) return;
    
    document.getElementById('detail-title').innerText = item.title;
    document.getElementById('detail-author').innerText = item.author;
    document.getElementById('detail-date').innerText = item.date;
    document.getElementById('detail-content').innerText = item.content;
    
    const fileArea = document.getElementById('detail-file-area');
    const fileNameSpan = document.getElementById('detail-file-name');
    
    if(item.fileName) {
        fileArea.style.display = 'block';
        fileNameSpan.innerText = item.fileName;
        fileNameSpan.onclick = () => alert("가상 첨부파일 다운로드 시뮬레이션입니다.");
    } else {
        fileArea.style.display = 'none';
    }
    
    document.getElementById('board-detail-modal-overlay').style.display = 'flex';
}

function closeBoardDetail() {
    document.getElementById('board-detail-modal-overlay').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', () => {
    // Add overlay click events for board
    const overlays = ['board-list-modal-overlay', 'board-create-modal-overlay', 'board-detail-modal-overlay'];
    overlays.forEach(id => {
        const el = document.getElementById(id);
        if(el) {
            el.addEventListener('click', (e) => {
                if(e.target.id === id) {
                    if(id === 'board-list-modal-overlay') closeBoardList();
                    if(id === 'board-create-modal-overlay') closeBoardCreate();
                    if(id === 'board-detail-modal-overlay') closeBoardDetail();
                }
            });
        }
    });
});
"""

with open("main.js", "a", encoding="utf-8") as f:
    f.write(js_addition)

print("Board implemented.")
