import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Separate Inquiry Section
support_to_inquiry = """                </div>
                
                <!-- Inquiry Form -->
                <div class="inquiry-form-container fade-up" id="inquiry">"""

new_support_to_inquiry = """                </div>
            </div>
        </div>
    </section>

    <!-- 5. 문의하기 (Inquiry) -->
    <section id="inquiry" class="inquiry section bg-white">
        <div class="container">
            <div class="section-header text-center fade-up">
                <h2 class="section-title">문의하기</h2>
                <p>Inquiry</p>
            </div>
            <div class="contact-layout mt-5" style="justify-content: center;">
                <!-- Inquiry Form -->
                <div class="inquiry-form-container fade-up" style="flex: 0 0 100%; max-width: 800px; margin: 0 auto;">"""

html = html.replace(support_to_inquiry, new_support_to_inquiry)

# 2. Change col-md-4 to col-md-6
start_idx = html.find('<!-- 3. 자료실 (Reference) -->')
if start_idx != -1:
    end_idx = html.find('<!-- 4. 고객지원 (Customer Support) -->', start_idx)
    ref_html = html[start_idx:end_idx]
    new_ref_html = ref_html.replace('col-md-4 mb-4', 'col-md-6 mb-4')
    html = html.replace(ref_html, new_ref_html)

# 3. Add PDF Download Button to Modal
pdf_modal_header = """            <div style="background:#f8f9fa; padding:15px; border-bottom:1px solid #ddd;">
                <h4 id="pdf-modal-title" style="margin:0; font-size:1.2rem; color:var(--primary-blue);">문서 뷰어</h4>
            </div>"""

new_pdf_modal_header = """            <div style="background:#f8f9fa; padding:15px; border-bottom:1px solid #ddd; display:flex; justify-content:space-between; align-items:center;">
                <h4 id="pdf-modal-title" style="margin:0; font-size:1.2rem; color:var(--primary-blue);">문서 뷰어</h4>
                <a id="pdf-download-btn" href="#" download class="btn btn-primary btn-sm" style="margin-right:30px; font-weight:bold;"><i class="ph-bold ph-download-simple"></i> PDF 다운로드</a>
            </div>"""

html = html.replace(pdf_modal_header, new_pdf_modal_header)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)


# Update JS for download button
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

if "downloadBtn.href = pdfUrl;" not in js:
    # insert inside openPdfModal
    js = js.replace("iframe.src = pdfUrl;", "iframe.src = pdfUrl;\n        const downloadBtn = document.getElementById('pdf-download-btn');\n        if(downloadBtn) downloadBtn.href = pdfUrl;")

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Files updated.")
