import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# I will replace the exact block to wrap the video and text
old_block = """            <div class="about-grid mt-4">
                
                <!-- 홍보 영상 -->
                <div class="promo-video-container mb-4 fade-up" style="position: relative; width: 100%; border-radius: 8px; overflow: hidden; box-shadow: var(--shadow-sm);">
                    <video id="promo-video" src="promo_video.mp4" style="width: 100%; display: block;" muted loop playsinline></video>
                    
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
                <p style="font-size: 0.8rem; color: #aaa; text-align: right; margin-top: 8px; margin-bottom: 0;">본 영상은 AI로 제작되었습니다.</p>"""

new_block = """            <div class="about-grid mt-4">
                
                <!-- 왼쪽: 홍보 영상 -->
                <div class="fade-up">
                    <div class="promo-video-container" style="position: relative; width: 100%; border-radius: 8px; overflow: hidden; box-shadow: var(--shadow-sm);">
                        <video id="promo-video" src="promo_video.mp4" style="width: 100%; display: block;" muted loop playsinline></video>
                        
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
                    <p style="font-size: 0.8rem; color: #aaa; text-align: right; margin-top: 8px; margin-bottom: 0;">본 영상은 AI로 제작되었습니다.</p>
                </div>"""

if old_block in html:
    html = html.replace(old_block, new_block)
else:
    print("Failed to find block. Attempting fallback regex.")
    
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTML layout updated.")
