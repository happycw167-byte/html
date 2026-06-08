import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

start_idx = html.find('<!-- 2. 장비 및 시설 (Equipment & Facilities) -->')
end_idx = html.find('<!-- 3. 자료실 (Reference) -->')

if start_idx != -1 and end_idx != -1:
    eq_html = html[start_idx:end_idx]
    
    # Clean out ALL occurrences of hidden-equipment first
    eq_html = eq_html.replace(' hidden-equipment', '')
    
    # We want to find exactly all tags starting with <div class="equipment-item
    # and add hidden-equipment to the 9th, 10th, ... 16th.
    
    pattern = r'<div class="equipment-item'
    matches = list(re.finditer(pattern, eq_html))
    
    print(f"Found {len(matches)} items.")
    if len(matches) == 16:
        for m in reversed(matches[8:]): 
            pos = m.end()
            eq_html = eq_html[:pos] + ' hidden-equipment' + eq_html[pos:]
            
    html = html[:start_idx] + eq_html + html[end_idx:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done.")
