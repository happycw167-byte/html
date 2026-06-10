with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

# We want to remove lines 172, 275, and 276.
# Note: Python lines are 0-indexed.
# So line 172 is index 171
# Line 275 is index 274
# Line 276 is index 275
# To remove safely without shifting indices during deletion, we should iterate or build a new list.

new_lines = []
for i, line in enumerate(lines):
    # Change video src
    if 'src="promo_video.mp4"' in line:
        line = line.replace('src="promo_video.mp4"', 'src="engineer_pump.mp4"')
        
    # Check if we should drop this line to fix the layout overlap
    if i == 171 and line.strip() == "</div>":
        continue
    if i == 274 and line.strip() == "</div>":
        continue
    if i == 275 and line.strip() == "</div>":
        continue
        
    new_lines.append(line)

with open("index.html", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("HTML fixed.")
