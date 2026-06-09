import re

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

video_html = """
                <!-- 홍보 영상 -->
                <div class="promo-video-container mb-4 fade-up" style="position: relative; width: 100%; border-radius: 8px; overflow: hidden; box-shadow: var(--shadow-sm);">
                    <video id="promo-video" src="홍보영상.mp4" style="width: 100%; display: block;" muted autoplay loop playsinline></video>
                    
                    <!-- 커스텀 컨트롤 버튼 -->
                    <div style="position: absolute; bottom: 15px; right: 15px; display: flex; gap: 10px; z-index: 10;">
                        <button id="btn-video-play" class="btn btn-primary" style="padding: 8px 15px; font-weight: bold; display: none; background: rgba(0,0,0,0.6); border: none;">
                            <i class="ph-fill ph-play" style="color:white;"></i> <span style="color:white;">재생</span>
                        </button>
                        <button id="btn-video-pause" class="btn btn-secondary" style="padding: 8px 15px; font-weight: bold; background: rgba(0,0,0,0.6); border: none;">
                            <i class="ph-fill ph-pause" style="color:white;"></i> <span style="color:white;">정지</span>
                        </button>
                    </div>
                </div>
                
                <!-- CEO 인사말 -->
"""

html = html.replace('<!-- CEO 인사말 -->', video_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)


# 2. Update main.js
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

js_addition = """
document.addEventListener('DOMContentLoaded', () => {
    // --- 홍보영상 컨트롤 로직 ---
    const promoVideo = document.getElementById('promo-video');
    const btnPlay = document.getElementById('btn-video-play');
    const btnPause = document.getElementById('btn-video-pause');

    if (promoVideo && btnPlay && btnPause) {
        btnPlay.addEventListener('click', () => {
            promoVideo.play();
            btnPlay.style.display = 'none';
            btnPause.style.display = 'inline-block';
        });

        btnPause.addEventListener('click', () => {
            promoVideo.pause();
            btnPause.style.display = 'none';
            btnPlay.style.display = 'inline-block';
        });
    }
});
"""

js += "\n" + js_addition

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Video features added.")
