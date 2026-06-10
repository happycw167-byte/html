from PIL import Image
import re

def remove_white_bg(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    data = img.getdata()
    
    new_data = []
    # Smooth thresholding for anti-aliasing
    for item in data:
        r, g, b, a = item
        # If the pixel is very bright, reduce its alpha
        # Calculate brightness
        brightness = (r + g + b) / 3
        if brightness > 220:
            # Scale alpha: 220 -> 255, 255 -> 0
            # alpha = 255 - (brightness - 220) * (255 / 35)
            alpha = int(255 - (brightness - 220) * 7.28)
            new_data.append((r, g, b, max(0, alpha)))
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    img.save(output_path, "PNG")

try:
    remove_white_bg("company_logo.jpeg", "company_logo.png")
    print("company_logo.png created with transparent background.")
    
    # Update index.html
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    html = html.replace('src="company_logo.jpeg"', 'src="company_logo.png"')
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html updated to use company_logo.png.")
except Exception as e:
    print("Error:", e)
