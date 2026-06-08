import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# We need to extract the map-container from inside contact-info and put it right after it.
# The contact-info block ends after the map-container with two </div>'s in the current setup.
# Actually, let's just find the exact block and replace it.

old_block = """                    </ul>

                    <!-- 구글 지도 연동 -->
                    <div class="map-container mb-4" style="margin-top: 30px; height: 300px; border-radius: 8px; overflow: hidden; box-shadow: var(--shadow-sm); border: 1px solid var(--border-color);">
                        <iframe 
                            src="https://maps.google.com/maps?q=강원특별자치도%20춘천시%20퇴계공단2길%2064&t=&z=16&ie=UTF8&iwloc=&output=embed" 
                            width="100%" 
                            height="100%" 
                            style="border:0;" 
                            allowfullscreen="" 
                            loading="lazy">
                        </iframe>
                    </div>

                    
                </div>
            </div>"""

new_block = """                    </ul>
                </div>

                <!-- 구글 지도 연동 -->
                <div class="map-container fade-up" style="height: 100%; min-height: 350px; border-radius: 8px; overflow: hidden; box-shadow: var(--shadow-sm); border: 1px solid var(--border-color);">
                    <iframe 
                        src="https://maps.google.com/maps?q=강원특별자치도%20춘천시%20퇴계공단2길%2064&t=&z=16&ie=UTF8&iwloc=&output=embed" 
                        width="100%" 
                        height="100%" 
                        style="border:0;" 
                        allowfullscreen="" 
                        loading="lazy">
                    </iframe>
                </div>
            </div>"""

if old_block in html:
    html = html.replace(old_block, new_block)
else:
    print("Could not find the exact block.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Map moved to the right column.")
