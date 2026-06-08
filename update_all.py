import re

def update_html():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Logos
    html = html.replace('<i class="ph-fill ph-drop text-primary"></i> BEATECH', '<img src="company_logo.jpeg" alt="로고" style="height:30px; margin-right:8px;"> 비에이텍(주)')
    html = html.replace('<i class="ph-fill ph-drop"></i> BEATECH', '<img src="company_logo.jpeg" alt="로고" style="height:30px; margin-right:8px;"> 비에이텍(주)')

    # 2. Timeline items visibility
    # We want to add the class `hidden-achievement` to items after the 5th item.
    # The achievements section starts after `<!-- 주요사업 실적 -->`
    start_idx = html.find('<!-- 주요사업 실적 -->')
    if start_idx != -1:
        timeline_start = html.find('<div class="timeline">', start_idx)
        timeline_end = html.find('</div>', html.find('</div>', html.find('</div>', timeline_start) + 1) + 1) # This isn't reliable, let's use regex
        
        # Split the HTML at `<!-- 주요사업 실적 -->`
        html_pre = html[:timeline_start]
        html_post = html[timeline_start:]
        
        # Find the end of this timeline block. 
        # The end is right before `<!-- 인증 및 수상 -->` or `</div>\n                            </div>\n                        </div>\n                    </div>`
        timeline_end_idx = html_post.find('</div>\n                            </div>')
        achievements_block = html_post[:timeline_end_idx]
        
        # Now replace items 6 to 16 in achievements_block
        items = re.split(r'(<div class="timeline-item">)', achievements_block)
        # items[0] is `<div class="timeline">\n`
        # items[1] is `<div class="timeline-item">`
        # items[2] is content of item 1
        # etc...
        # So item 1 is items[1]+items[2], item 2 is items[3]+items[4], etc.
        # We want to add `hidden-achievement` to `items[i]` where i >= 11 (which is the 6th item)
        new_achievements_block = items[0]
        for i in range(1, len(items), 2):
            if i >= 11:
                new_achievements_block += '<div class="timeline-item hidden-achievement">' + items[i+1]
            else:
                new_achievements_block += items[i] + items[i+1]
                
        # Append toggle button
        toggle_button = '\n                                </div>\n                                <div class="text-center mt-3"><button id="btn-toggle-achievements" class="btn btn-outline btn-sm" style="border-color:var(--primary-blue); color:var(--primary-blue);">더보기 (▼)</button></div>'
        new_achievements_block = new_achievements_block.replace('                                </div>', toggle_button, 1)

        html = html_pre + new_achievements_block + html_post[timeline_end_idx:]

    # 3. References to open in Modal
    # Replace target="_blank" with onclick="openPdfModal('URL')" for PDFs
    def replace_pdf_link(m):
        url = m.group(1)
        # remove target="_blank" and change href
        return f'<a href="javascript:void(0)" onclick="openPdfModal(\'{url}\')" class="card shadow-sm text-decoration-none">'

    html = re.sub(r'<a href="([^"]+\.pdf)" target="_blank" class="card shadow-sm text-decoration-none">', replace_pdf_link, html)

    # 4. Add PDF Modal HTML at the end of body
    pdf_modal_html = """
    <!-- PDF Viewer Modal -->
    <div id="pdf-modal" class="cert-modal-wrapper">
        <div class="cert-modal-overlay" onclick="closePdfModal()"></div>
        <div class="pdf-modal-content" style="position:relative; width:90%; height:90vh; max-width:1200px; z-index:10001; background:white; border-radius:8px; overflow:hidden;">
            <button class="cert-modal-close" onclick="closePdfModal()" aria-label="닫기" style="position:absolute; top:10px; right:15px; color:#333; z-index:10002;">
                <i class="ph ph-x"></i>
            </button>
            <div style="background:#f8f9fa; padding:15px; border-bottom:1px solid #ddd;">
                <h4 id="pdf-modal-title" style="margin:0; font-size:1.2rem; color:var(--primary-blue);">문서 뷰어</h4>
            </div>
            <iframe id="pdf-modal-iframe" src="" style="width:100%; height:calc(100% - 60px); border:none;"></iframe>
        </div>
    </div>
"""
    if 'id="pdf-modal"' not in html:
        html = html.replace('</body>', pdf_modal_html + '\n</body>')

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)


def update_css():
    with open("style.css", "a", encoding="utf-8") as f:
        f.write("""
/* Hidden Achievement Toggle */
.hidden-achievement {
    display: none;
}
""")

def update_js():
    with open("main.js", "a", encoding="utf-8") as f:
        f.write("""
// Achievement Toggle Logic
document.addEventListener('DOMContentLoaded', () => {
    const btnToggle = document.getElementById('btn-toggle-achievements');
    if (btnToggle) {
        btnToggle.addEventListener('click', () => {
            const hiddenItems = document.querySelectorAll('.timeline-item.hidden-achievement, .timeline-item.shown-achievement');
            let isShowingAll = btnToggle.innerText.includes('접기');
            
            if (isShowingAll) {
                // Hide them
                hiddenItems.forEach(item => {
                    item.classList.remove('shown-achievement');
                    item.classList.add('hidden-achievement');
                    item.style.display = 'none';
                });
                btnToggle.innerText = '더보기 (▼)';
            } else {
                // Show them
                hiddenItems.forEach(item => {
                    item.classList.remove('hidden-achievement');
                    item.classList.add('shown-achievement');
                    item.style.display = 'block';
                });
                btnToggle.innerText = '접기 (▲)';
            }
        });
    }
});

// PDF Modal Logic
window.openPdfModal = function(pdfUrl) {
    const modal = document.getElementById('pdf-modal');
    const iframe = document.getElementById('pdf-modal-iframe');
    const title = document.getElementById('pdf-modal-title');
    
    if (modal && iframe) {
        // extract filename for title
        let filename = pdfUrl.split('/').pop().replace('.pdf', '');
        filename = decodeURIComponent(filename);
        if (title) title.innerText = filename;
        
        iframe.src = pdfUrl;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
};

window.closePdfModal = function() {
    const modal = document.getElementById('pdf-modal');
    const iframe = document.getElementById('pdf-modal-iframe');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        if (iframe) iframe.src = '';
    }
};
""")

update_html()
update_css()
update_js()
print("All files updated successfully.")
