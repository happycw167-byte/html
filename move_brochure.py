import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Move Brochure to the right of '편흡입볼류트펌프 유지관리지침서'
# Extract the brochure HTML block
brochure_pattern = r'                    <a href="javascript:void\(0\)" onclick="openCertModal\(\'brochure\.png\'\)" class="card shadow-sm text-decoration-none checkerboard-item">.*?</a>\s*'
brochure_match = re.search(brochure_pattern, html, flags=re.DOTALL)
if brochure_match:
    brochure_html = brochure_match.group(0)
    # Remove it from its current position
    html = html.replace(brochure_html, "")
    
    # Find the end of '편흡입볼류트펌프 유지관리지침서'
    target_pattern = r'                    <a href="javascript:void\(0\)" onclick="openPdfModal\(\'\./편흡입볼류트펌프 유지관리지침서\.pdf\'\)" class="card shadow-sm text-decoration-none checkerboard-item">.*?</a>\n'
    target_match = re.search(target_pattern, html, flags=re.DOTALL)
    if target_match:
        target_full = target_match.group(0)
        # Append brochure after it
        html = html.replace(target_full, target_full + brochure_html)
        print("Brochure moved successfully.")
    else:
        print("Could not find the target '편흡입볼류트펌프 유지관리지침서'.")
else:
    print("Could not find brochure HTML.")

# 2. Add download button to cert-modal
# <img id="cert-modal-img" src="" alt="인증서 확대 이미지">
old_modal_img = '<img id="cert-modal-img" src="" alt="인증서 확대 이미지">'
new_modal_img = old_modal_img + '\n            <div style="text-align: center; margin-top: 15px;"><a id="cert-download-btn" href="" download class="btn btn-primary"><i class="ph-fill ph-download-simple"></i> 다운로드</a></div>'

if old_modal_img in html and 'id="cert-download-btn"' not in html:
    html = html.replace(old_modal_img, new_modal_img)
    print("Download button added to cert-modal.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

# 3. Update main.js to set the href of cert-download-btn
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Update openCertModal
old_cert_modal = """window.openCertModal = function(imgSrc) {
    const modal = document.getElementById('cert-modal');
    const modalImg = document.getElementById('cert-modal-img');
    if (modal && modalImg) {
        modalImg.src = imgSrc;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
};"""

new_cert_modal = """window.openCertModal = function(imgSrc) {
    const modal = document.getElementById('cert-modal');
    const modalImg = document.getElementById('cert-modal-img');
    const downloadBtn = document.getElementById('cert-download-btn');
    if (modal && modalImg) {
        modalImg.src = imgSrc;
        if (downloadBtn) {
            downloadBtn.href = imgSrc;
        }
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
};"""

if old_cert_modal in js:
    js = js.replace(old_cert_modal, new_cert_modal)
    with open("main.js", "w", encoding="utf-8") as f:
        f.write(js)
    print("main.js updated for cert-download-btn.")
else:
    print("Could not find old openCertModal in main.js.")
