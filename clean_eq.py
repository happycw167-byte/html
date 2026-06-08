import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

start_idx = html.find('<!-- 2. 장비 및 시설 (Equipment) -->')
end_idx = html.find('<!-- 3. 자료실 (Reference) -->')

if start_idx != -1 and end_idx != -1:
    eq_html = html[start_idx:end_idx]
    
    # We will find all <div class="equipment-item ...">
    # and rewrite them cleanly.
    
    # 1. Clean out all hidden-equipment
    eq_html = eq_html.replace(' hidden-equipment', '')
    
    # 2. Split by equipment-item and add it back to items 9 through 16 (index 9 to 16 in parts array)
    parts = eq_html.split('<div class="equipment-item')
    
    for i in range(9, len(parts)):
        # Usually starts with ' fade-up"' or ' fade-up" style=...'
        if parts[i].startswith(' fade-up"'):
            parts[i] = parts[i].replace(' fade-up"', ' fade-up hidden-equipment"', 1)
        elif parts[i].startswith(' fade-up '):
            # just in case
            parts[i] = parts[i].replace(' fade-up ', ' fade-up hidden-equipment ', 1)
            
    new_eq_html = '<div class="equipment-item'.join(parts)
    html = html.replace(eq_html, new_eq_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Cleaned up equipment items.")
