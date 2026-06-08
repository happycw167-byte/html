import re

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find the board-list-modal header to add the '선택' button
old_header = """<button onclick="closeBoardList()" style="background:none; border:none; font-size:1.5rem; cursor:pointer; color:#fff;">&times;</button>"""
new_header = """
                <div>
                    <button id="btn-board-select-mode" onclick="toggleSelectMode()" style="background:rgba(255,255,255,0.2); border:1px solid rgba(255,255,255,0.5); font-size:0.9rem; cursor:pointer; color:#fff; padding:4px 10px; border-radius:4px; margin-right:15px; font-weight:bold;">선택</button>
                    <button onclick="closeBoardList()" style="background:none; border:none; font-size:1.5rem; cursor:pointer; color:#fff;">&times;</button>
                </div>
"""
html = html.replace(old_header, new_header)

# Add Delete Confirm Modal
delete_modal = """
    <!-- 게시물 삭제 확인 모달 -->
    <div id="board-delete-modal-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:2500; align-items:center; justify-content:center;">
        <div id="board-delete-modal" style="background:#fff; width:90%; max-width:350px; border-radius:12px; overflow:hidden; box-shadow:0 15px 30px rgba(0,0,0,0.2); text-align:center;">
            <div style="background:var(--primary-blue); color:#fff; padding:15px; font-weight:bold;">
                알림
            </div>
            <div style="padding: 30px 20px;">
                <h4 style="margin-bottom: 20px; color:#333; font-weight:bold;">삭제</h4>
                <p style="color:#666; margin-bottom:30px; font-size:0.9rem;">해당 공지사항을 삭제하시겠습니까?</p>
                <div style="display:flex; justify-content:center; gap:10px;">
                    <button onclick="closeDeleteConfirm()" class="btn btn-secondary" style="padding: 8px 25px;">취소</button>
                    <button onclick="confirmDeleteBoard()" class="btn btn-danger" style="padding: 8px 25px;">예</button>
                </div>
            </div>
        </div>
    </div>
"""

html = html.replace('</body>', delete_modal + '\n</body>')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

# 2. Update main.js
js_addition = """
let isSelectMode = false;
let deleteTargetId = null;

function toggleSelectMode() {
    isSelectMode = !isSelectMode;
    const btn = document.getElementById('btn-board-select-mode');
    
    if (isSelectMode) {
        btn.innerText = '취소';
        btn.style.background = '#dc3545'; // red to indicate delete mode
        btn.style.borderColor = '#dc3545';
        document.getElementById('board-list-body').style.cursor = 'crosshair';
        alert("선택 모드가 켜졌습니다. 삭제할 공지사항을 클릭해주세요.");
    } else {
        btn.innerText = '선택';
        btn.style.background = 'rgba(255,255,255,0.2)';
        btn.style.borderColor = 'rgba(255,255,255,0.5)';
        document.getElementById('board-list-body').style.cursor = 'default';
    }
}

// We need to overwrite renderBoard() to handle isSelectMode
// Since we appended renderBoard() earlier, we can just redefine it (or replace the string in the file).
// It's safer to read and replace the old renderBoard function in main.js.
"""

# Let's read main.js and replace renderBoard to include the new logic
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

old_render = """        tr.onclick = () => openBoardDetail(item.id);"""
new_render = """        tr.onclick = () => {
            if (isSelectMode) {
                openDeleteConfirm(item.id);
            } else {
                openBoardDetail(item.id);
            }
        };"""
js = js.replace(old_render, new_render)

# Add new functions for delete
delete_functions = """
function openDeleteConfirm(id) {
    deleteTargetId = id;
    document.getElementById('board-delete-modal-overlay').style.display = 'flex';
}

function closeDeleteConfirm() {
    deleteTargetId = null;
    document.getElementById('board-delete-modal-overlay').style.display = 'none';
}

function confirmDeleteBoard() {
    if (deleteTargetId !== null) {
        boardData = boardData.filter(item => item.id !== deleteTargetId);
        localStorage.setItem('boardData', JSON.stringify(boardData));
        closeDeleteConfirm();
        renderBoard();
        
        // Disable select mode after deletion for safety
        if(isSelectMode) toggleSelectMode();
    }
}
"""
js += "\n" + js_addition + "\n" + delete_functions

# Also add the new modal to the overlay click event
replace_overlays = "const overlays = ['board-list-modal-overlay', 'board-create-modal-overlay', 'board-detail-modal-overlay'];"
new_overlays = "const overlays = ['board-list-modal-overlay', 'board-create-modal-overlay', 'board-detail-modal-overlay', 'board-delete-modal-overlay'];"
js = js.replace(replace_overlays, new_overlays)

replace_close = "if(id === 'board-detail-modal-overlay') closeBoardDetail();"
new_close = "if(id === 'board-detail-modal-overlay') closeBoardDetail();\n                    if(id === 'board-delete-modal-overlay') closeDeleteConfirm();"
js = js.replace(replace_close, new_close)


with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Delete functionality added.")
