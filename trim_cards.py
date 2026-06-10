from PIL import Image

def trim_and_square(filename, output_name):
    im = Image.open(filename).convert('RGB')
    
    # Convert to grayscale to find white background
    gray = im.convert('L')
    # Anything lighter than 240 is considered background (white)
    # We want bounding box of non-white
    bg = gray.point(lambda p: 0 if p > 240 else 255)
    
    bbox = bg.getbbox()
    if bbox:
        # Bounding box is (left, upper, right, lower)
        cropped = im.crop(bbox)
        
        # Make it exactly 1:1 by center cropping the minimum dimension
        w, h = cropped.size
        min_dim = min(w, h)
        cx = w // 2
        cy = h // 2
        
        square = cropped.crop((cx - min_dim//2, cy - min_dim//2, cx + min_dim//2, cy + min_dim//2))
        square.save(output_name)
        print(f"Trimmed and saved {output_name}")
    else:
        # If no bounding box found, just use the original image
        im.save(output_name)
        print(f"Saved original {output_name}")

# Correct order:
# card_1 = chatgpt_2 (Page 1)
# card_2 = slice1_1 (Page 2)
# card_3 = slice1_2 (Page 3)
# card_4 = slice1_3 (Page 4)
# card_5 = slice1_4 (Page 5)

import shutil
shutil.copy("chatgpt_2.png", "card_1.png")
print("Saved card_1.png (Page 1)")

trim_and_square("slice1_1.png", "card_2.png")
trim_and_square("slice1_2.png", "card_3.png")
trim_and_square("slice1_3.png", "card_4.png")
trim_and_square("slice1_4.png", "card_5.png")

print("All cards processed and reordered.")
