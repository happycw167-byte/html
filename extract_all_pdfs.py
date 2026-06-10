import os
import json
import fitz # PyMuPDF
import easyocr

def extract_pdf_data():
    print("Initializing EasyOCR...")
    reader = easyocr.Reader(['ko', 'en'])
    
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    new_knowledge = []
    
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        try:
            doc = fitz.open(pdf_file)
            
            for i, page in enumerate(doc):
                # Try direct text extraction first
                text = page.get_text()
                
                # If text is very short, assume it's an image-based page
                if len(text.strip()) < 50:
                    print(f"  Page {i+1}: Image detected, running OCR...")
                    pix = page.get_pixmap(dpi=150)
                    img_bytes = pix.tobytes("png")
                    # OCR
                    ocr_results = reader.readtext(img_bytes, detail=0)
                    text = " ".join(ocr_results)
                
                # Clean up text and chunk it
                text = text.replace('\n', ' ').strip()
                if text:
                    # Break into chunks of ~500 chars to avoid massive single entries
                    words = text.split()
                    chunk = []
                    chunk_len = 0
                    for word in words:
                        chunk.append(word)
                        chunk_len += len(word) + 1
                        if chunk_len > 500:
                            new_knowledge.append({
                                "source": pdf_file,
                                "text": " ".join(chunk)
                            })
                            chunk = []
                            chunk_len = 0
                    
                    if chunk:
                        new_knowledge.append({
                            "source": pdf_file,
                            "text": " ".join(chunk)
                        })
                        
            print(f"Finished {pdf_file}")
            
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")
            
    # Update knowledge_base.js
    kb_file = 'knowledge_base.js'
    try:
        with open(kb_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract JSON part
        start_idx = content.find('[')
        end_idx = content.rfind(']') + 1
        
        if start_idx != -1 and end_idx != -1:
            json_str = content[start_idx:end_idx]
            kb_list = json.loads(json_str)
            
            # Remove all old PDF entries
            kb_list = [item for item in kb_list if not item.get('source', '').endswith('.pdf')]
            
            # Add new PDF entries
            kb_list.extend(new_knowledge)
            
            # Write back
            new_json_str = json.dumps(kb_list, ensure_ascii=False, indent=4)
            new_content = content[:start_idx] + new_json_str + content[end_idx:]
            
            with open(kb_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            print("Successfully updated knowledge_base.js")
            print(f"Total entries in knowledge_base: {len(kb_list)}")
            
    except Exception as e:
        print(f"Error updating knowledge_base.js: {e}")

if __name__ == "__main__":
    extract_pdf_data()
