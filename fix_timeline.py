with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

bad_snippet = """                                        <div class="timeline-year">2019</div>
                                        <div class="timeline-content">김화하수처리구역(와수3처리분구) 하수관거정비사업 수중볼텍스펌프 (철원군상하수도사업소)</div>
                                    </div>
    
                                </div>
                                <div class="text-center mt-3"><button id="btn-toggle-achievements" class="btn btn-outline btn-sm" style="border-color:var(--primary-blue); color:var(--primary-blue);">더보기 (▼)</button></div>
                                    <div class="timeline-item">"""

good_snippet = """                                        <div class="timeline-year">2019</div>
                                        <div class="timeline-content">김화하수처리구역(와수3처리분구) 하수관거정비사업 수중볼텍스펌프 (철원군상하수도사업소)</div>
                                    </div>
                                    <div class="timeline-item">"""

# Remove the bad button
html = html.replace(bad_snippet, good_snippet)

# Add the button at the correct end
end_snippet = """                                        <div class="timeline-year">2019</div>
                                        <div class="timeline-content">철원군 화지리(2,3처리분구) 하수관거정비사업 수중볼텍스펌프 (철원군상하수도사업소)</div>
                                    </div>
                                </div>"""

fixed_end_snippet = """                                        <div class="timeline-year">2019</div>
                                        <div class="timeline-content">철원군 화지리(2,3처리분구) 하수관거정비사업 수중볼텍스펌프 (철원군상하수도사업소)</div>
                                    </div>
                                </div>
                                <div class="text-center mt-3"><button id="btn-toggle-achievements" class="btn btn-outline btn-sm" style="border-color:var(--primary-blue); color:var(--primary-blue);">더보기 (▼)</button></div>"""

html = html.replace(end_snippet, fixed_end_snippet)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
