import re

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1) Update Video Tag (remove autoplay)
html = html.replace('muted autoplay loop playsinline', 'muted loop playsinline')

# 2) Add AI text
ai_text = '<p style="font-size: 0.8rem; color: #aaa; text-align: right; margin-top: 8px; margin-bottom: 0;">본 영상은 AI로 제작되었습니다.</p>'
html = html.replace('</div>\n                \n                <!-- CEO 인사말 -->', '</div>\n                ' + ai_text + '\n                \n                <!-- CEO 인사말 -->')

# 3) Center Overview and Org Chart
replace_center_start = """                    <div class="ceo-sign mt-4">
                        <span>대표이사</span> <strong>조세연</strong>
                    </div>
                </div>
                
                <!-- 기업 개요 및 조직도 -->
                <div class="fade-up">"""
                
new_center_start = """                    <div class="ceo-sign mt-4">
                        <span>대표이사</span> <strong>조세연</strong>
                    </div>
                </div>
            </div> <!-- End of about-grid -->
                
            <!-- 기업 개요 및 조직도 (중앙 정렬) -->
            <div class="fade-up" style="max-width: 800px; margin: 80px auto 0 auto; text-align: center;">"""

if replace_center_start in html:
    html = html.replace(replace_center_start, new_center_start)
else:
    print("Could not find the target string for centering.")

# Center the ul.info-list
html = html.replace('<ul class="info-list" style="margin-top:0;">', '<ul class="info-list" style="margin-top:0; display: inline-block; text-align: left;">')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

# 4) Update JS for Intersection Observer
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

js_observer = """
        // 자동 재생 (화면에 보일 때)
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        promoVideo.play().then(() => {
                            btnPlay.style.display = 'none';
                            btnPause.style.display = 'inline-block';
                        }).catch(e => console.log('Autoplay prevented:', e));
                    } else {
                        promoVideo.pause();
                        btnPause.style.display = 'none';
                        btnPlay.style.display = 'inline-block';
                    }
                });
            }, { threshold: 0.5 });
            observer.observe(promoVideo);
        }
"""
if "if (promoVideo && btnPlay && btnPause) {" in js:
    js = js.replace("if (promoVideo && btnPlay && btnPause) {", "if (promoVideo && btnPlay && btnPause) {\n" + js_observer)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Updates completed.")
