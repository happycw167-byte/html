import fitz
import glob
import json

pdfs = glob.glob('*.pdf')
target = None
for p in pdfs:
    if '지명원' in p or '지명원' in p:
        target = p
        break

if not target:
    print("PDF not found!")
    exit(1)

doc = fitz.open(target)
extracted_data = []

img_idx = 1
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text("text").strip()
    
    images = page.get_images(full=True)
    img_paths = []
    for img in images:
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        img_name = f"profile_img_{page_num+1}_{img_idx}.{image_ext}"
        
        with open(img_name, "wb") as f:
            f.write(image_bytes)
        img_paths.append(img_name)
        img_idx += 1
        
    extracted_data.append({
        "page": page_num + 1,
        "text": text,
        "images": img_paths
    })

with open("profile_data.json", "w", encoding="utf-8") as f:
    json.dump(extracted_data, f, ensure_ascii=False, indent=4)

print("Profile extraction complete.")
