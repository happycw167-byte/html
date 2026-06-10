import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update brochure link to use openCertModal
old_brochure = '<a href="brochure.png" target="_blank" download="비에이텍_브로슈어.png"'
new_brochure = '<a href="javascript:void(0)" onclick="openCertModal(\'brochure.png\')"'
if old_brochure in html:
    html = html.replace(old_brochure, new_brochure)
else:
    print("Could not find brochure link to update.")

# 2. Insert carousel below org chart
# Find the end of the fade-up div
target = """                                </div>
                            </div>
                        </div>
                    </div>
                </div>"""
carousel_html = """                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
            <!-- 카드뉴스 (Carousel) -->
            <div class="card-news-section mt-5 pt-4 fade-up">
                <h3 class="mb-4 text-center">카드뉴스</h3>
                <div class="slider-container" style="position: relative; max-width: 450px; margin: 0 auto; overflow: hidden; border-radius: 12px; box-shadow: var(--shadow-md);">
                    <div class="slider-track" id="card-slider-track" style="display: flex; transition: transform 0.5s ease-in-out;">
                        <img src="card_1.png" style="width: 100%; flex-shrink: 0;" alt="카드뉴스 1">
                        <img src="card_2.png" style="width: 100%; flex-shrink: 0;" alt="카드뉴스 2">
                        <img src="card_3.png" style="width: 100%; flex-shrink: 0;" alt="카드뉴스 3">
                        <img src="card_4.png" style="width: 100%; flex-shrink: 0;" alt="카드뉴스 4">
                        <img src="card_5.png" style="width: 100%; flex-shrink: 0;" alt="카드뉴스 5">
                    </div>
                    <button class="slider-btn prev-btn" onclick="moveSlide(-1)" style="position: absolute; top: 50%; left: 10px; transform: translateY(-50%); background: rgba(0,0,0,0.5); color: white; border: none; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; z-index: 10;">&#10094;</button>
                    <button class="slider-btn next-btn" onclick="moveSlide(1)" style="position: absolute; top: 50%; right: 10px; transform: translateY(-50%); background: rgba(0,0,0,0.5); color: white; border: none; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; z-index: 10;">&#10095;</button>
                </div>
            </div>"""

if target in html:
    html = html.replace(target, carousel_html)
else:
    print("Could not find the target location to insert carousel.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html updated successfully.")

# 3. Add JS function to main.js
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

js_func = """
// 카드뉴스 슬라이더 기능
let currentSlide = 0;
window.moveSlide = function(direction) {
    const track = document.getElementById('card-slider-track');
    if (!track) return;
    const totalSlides = 5;
    currentSlide += direction;
    if (currentSlide < 0) currentSlide = totalSlides - 1;
    if (currentSlide >= totalSlides) currentSlide = 0;
    track.style.transform = `translateX(-${currentSlide * 100}%)`;
};
"""
if "window.moveSlide" not in js:
    with open("main.js", "a", encoding="utf-8") as f:
        f.write("\n" + js_func)
    print("main.js updated successfully.")
