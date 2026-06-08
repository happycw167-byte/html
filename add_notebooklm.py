import re

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the onclick for "NotebookLM 지침서"
old_onclick = "onclick=\"alert('NotebookLM 지침서 기능은 준비 중입니다.')\""
new_onclick = "onclick=\"openNotebookMenu()\""
html = html.replace(old_onclick, new_onclick)

modals_html = """
    <!-- NotebookLM 하위 메뉴 모달 -->
    <div id="notebook-menu-modal-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:2200; align-items:center; justify-content:center;">
        <div id="notebook-menu-modal" style="background:#fff; width:90%; max-width:400px; border-radius:12px; overflow:hidden; box-shadow:0 15px 30px rgba(0,0,0,0.2); text-align:center;">
            <div style="background:var(--primary-blue); color:#fff; padding:15px; display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; font-size:1.2rem; color:#fff;"><i class="ph-fill ph-book-open-text"></i> NotebookLM</h4>
                <button onclick="closeNotebookMenu()" style="background:none; border:none; font-size:1.5rem; cursor:pointer; color:#fff;">&times;</button>
            </div>
            <div style="padding: 30px 20px;">
                <p style="color:#666; margin-bottom:25px;">원하시는 항목을 선택해주세요.</p>
                <div style="display:flex; flex-direction:column; gap:15px;">
                    <button onclick="openPromptGuide()" class="btn btn-primary" style="padding:15px; font-size:1.1rem; font-weight:bold; border-radius:8px;">
                        <i class="ph-bold ph-lightbulb" style="margin-right:8px;"></i> 프롬프트 작성 가이드
                    </button>
                    <button onclick="window.open('https://notebooklm.google.com/', '_blank')" class="btn" style="background-color:#2e7d32; color:white; padding:15px; font-size:1.1rem; font-weight:bold; border-radius:8px; border:none;">
                        <i class="ph-bold ph-arrow-square-out" style="margin-right:8px;"></i> NotebookLM 바로가기
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- 프롬프트 가이드 모달 -->
    <div id="prompt-guide-modal-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:2300; align-items:center; justify-content:center;">
        <div id="prompt-guide-modal" style="background:#f8f9fa; width:90%; max-width:800px; height:85vh; max-height:800px; border-radius:12px; overflow:hidden; box-shadow:0 15px 30px rgba(0,0,0,0.2); display:flex; flex-direction:column;">
            <div style="background:var(--primary-blue); color:#fff; padding:15px 20px; display:flex; justify-content:space-between; align-items:center; flex-shrink:0;">
                <h4 style="margin:0; font-size:1.2rem; color:#fff;"><i class="ph-fill ph-lightbulb"></i> 생성형 AI 프롬프트 작성 가이드</h4>
                <button onclick="closePromptGuide()" style="background:none; border:none; font-size:1.5rem; cursor:pointer; color:#fff;">&times;</button>
            </div>
            <div style="padding: 30px; overflow-y: auto; flex-grow:1; text-align:left;">
                
                <div style="background:#fff; padding:20px; border-radius:8px; border:1px solid #dee2e6; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                    <h5 style="color:var(--primary-blue); font-weight:bold;">1. 역할 부여</h5>
                    <p style="margin:10px 0 0 0; color:#444;">"당신은 세계적인 경영컨설턴트입니다. 중소기업의 디지털 전환 전략에 대해 조언해주세요."</p>
                </div>

                <div style="background:#fff; padding:20px; border-radius:8px; border:1px solid #dee2e6; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                    <h5 style="color:var(--primary-blue); font-weight:bold;">2. 명확성과 구체성 제공</h5>
                    <ul style="margin:10px 0 0 0; padding-left:20px; color:#444;">
                        <li><strong style="color:#dc3545;">나쁜 예:</strong> "보고서 좀 작성해줘"</li>
                        <li><strong style="color:#198754;">좋은 예:</strong> "2023년 의료AI 시장의 성장 트렌드에 대한 5페이지 분석 보고서를 작성해줘. 주요 기업, 투자 동향, 기술 혁신을 포함하고, 결론에서는 향후 3년간의 전망을 제시해줘."</li>
                    </ul>
                </div>

                <div style="background:#fff; padding:20px; border-radius:8px; border:1px solid #dee2e6; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                    <h5 style="color:var(--primary-blue); font-weight:bold;">3. 단계별 접근 요청</h5>
                    <p style="margin:10px 0 5px 0; color:#444;">다음 단계로 진행해주세요:</p>
                    <ul style="margin:0; padding-left:20px; color:#444;">
                        <li>머신러닝 프로젝트의 초기 데이터 탐색 방법 제시</li>
                        <li>필요한 전처리 단계 설명</li>
                        <li>모델 선택 기준 제시</li>
                        <li>성능 평가 메트릭스 추천</li>
                    </ul>
                </div>

                <div style="background:#fff; padding:20px; border-radius:8px; border:1px solid #dee2e6; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                    <h5 style="color:var(--primary-blue); font-weight:bold;">4. 출력 형식 명시</h5>
                    <p style="margin:10px 0 0 0; color:#444;">"[A4 페이지 2장 분량 / 1000 단어로], 학술적이고 간결한 형식의 보고서를 작성해줘. 들여쓰기와 APA 인용 스타일을 사용해줘."</p>
                </div>

                <div style="background:#fff; padding:20px; border-radius:8px; border:1px solid #dee2e6; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                    <h5 style="color:var(--primary-blue); font-weight:bold;">5. 컨텍스트와 제약 조건 제공</h5>
                    <p style="margin:10px 0 0 0; color:#444;">"의료 데이터 분석 시 환자 정보 보호법(HIPAA)을 준수하면서 연구 결과를 도출해줘."</p>
                </div>

                <div style="background:#fff; padding:20px; border-radius:8px; border:1px solid #dee2e6; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                    <h5 style="color:var(--primary-blue); font-weight:bold;">6. 예시와 대조 제공</h5>
                    <p style="margin:10px 0 0 0; color:#444;">"이런 방식의 분석은 피하고, 이런 접근 방식을 따라주세요."</p>
                </div>

                <div style="background:#fff; padding:20px; border-radius:8px; border:1px solid #dee2e6; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                    <h5 style="color:var(--primary-blue); font-weight:bold;">7. 반복 과정 제안</h5>
                    <ul style="margin:10px 0 0 0; padding-left:20px; color:#444;">
                        <li>구체적인 수정 사항 제시</li>
                        <li>부족한 부분 명확히 지적</li>
                        <li>추가 맥락 제공</li>
                    </ul>
                </div>

                <div style="background:#fff; padding:20px; border-radius:8px; border:1px solid #dee2e6; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                    <h5 style="color:var(--primary-blue); font-weight:bold;">8. 윤리적 고려사항 명시</h5>
                    <p style="margin:10px 0 0 0; color:#444;">"개인정보 보호, 공정성, 비차별적 언어 사용에 유의해주세요."</p>
                </div>

                <div style="background:#fff; padding:20px; border-radius:8px; border:1px solid #dee2e6; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                    <h5 style="color:var(--primary-blue); font-weight:bold;">9. 맥락 깊이 요구</h5>
                    <p style="margin:10px 0 0 0; color:#444;">"통계적 결과를 제시하는 것을 넘어, 그 결과가 실제 비즈니스 전략에 어떤 영향을 미치는지 설명해줘."</p>
                </div>

                <div style="background:#fff; padding:20px; border-radius:8px; border:1px solid #dee2e6; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                    <h5 style="color:var(--primary-blue); font-weight:bold;">10. 어조 / 형식</h5>
                    <ul style="margin:10px 0 0 0; padding-left:20px; color:#444;">
                        <li>"~이다". "~한다"와 같은 평서문으로 작성해줘.</li>
                        <li>"~임", "~함"과 같은 개조식으로 작성해줘.</li>
                    </ul>
                </div>

                <div style="background:#fff; padding:20px; border-radius:8px; border:1px solid #dee2e6; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                    <h5 style="color:var(--primary-blue); font-weight:bold;">11. 생성 과정 가이드</h5>
                    <ul style="margin:10px 0 0 0; padding-left:20px; color:#444;">
                        <li>Chain-of-Thought로 생각하고 순차적으로 생성해줘</li>
                        <li>토론 상황에서는 Devil's Advocate으로 나의 주장의 강점과 약점, 토론 상대의 예상 주장의 강점과 약점 및 반례 등을 정리해줘</li>
                    </ul>
                </div>

                <div style="background:#fff; padding:20px; border-radius:8px; border:1px solid #dee2e6; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                    <h5 style="color:var(--primary-blue); font-weight:bold;">12. 환각 최소화</h5>
                    <p style="margin:10px 0 0 0; color:#444;">본문에 참고한 출처는 반드시 명시하고 보고서 마지막에 참고문헌으로 정리해줘. 반드시 출처가 존재하는 참고문헌만을 명시해야 해.</p>
                </div>

                <div style="text-align:center; margin-top:30px;">
                    <button onclick="closePromptGuide()" class="btn btn-secondary">닫기</button>
                </div>
            </div>
        </div>
    </div>
"""

html = html.replace('</body>', modals_html + '\n</body>')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)


# 2. Update main.js
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

js_addition = """
function openNotebookMenu() {
    document.getElementById('notebook-menu-modal-overlay').style.display = 'flex';
}

function closeNotebookMenu() {
    document.getElementById('notebook-menu-modal-overlay').style.display = 'none';
}

function openPromptGuide() {
    // 프롬프트 가이드 열 때 이전 메뉴 닫기
    closeNotebookMenu();
    document.getElementById('prompt-guide-modal-overlay').style.display = 'flex';
}

function closePromptGuide() {
    document.getElementById('prompt-guide-modal-overlay').style.display = 'none';
}
"""

js += "\n" + js_addition

# Add click outside logic
replace_overlays = "const overlays = ['board-list-modal-overlay', 'board-create-modal-overlay', 'board-detail-modal-overlay', 'board-delete-modal-overlay'];"
new_overlays = "const overlays = ['board-list-modal-overlay', 'board-create-modal-overlay', 'board-detail-modal-overlay', 'board-delete-modal-overlay', 'notebook-menu-modal-overlay', 'prompt-guide-modal-overlay'];"
js = js.replace(replace_overlays, new_overlays)

replace_close = "if(id === 'board-delete-modal-overlay') closeDeleteConfirm();"
new_close = replace_close + """
                    if(id === 'notebook-menu-modal-overlay') closeNotebookMenu();
                    if(id === 'prompt-guide-modal-overlay') closePromptGuide();"""
js = js.replace(replace_close, new_close)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)

print("NotebookLM features added.")
