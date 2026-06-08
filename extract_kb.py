import glob
import json
import fitz
import re

def clean_html(raw_html):
    # Remove scripts and styles
    cleanr = re.compile('<script.*?>.*?</script>', re.DOTALL)
    text = re.sub(cleanr, '', raw_html)
    cleanr = re.compile('<style.*?>.*?</style>', re.DOTALL)
    text = re.sub(cleanr, '', text)
    # Remove HTML tags
    cleanr = re.compile('<.*?>')
    text = re.sub(cleanr, ' ', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

kb_chunks = []

# 1. Parse HTML
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    text = clean_html(html)
    # chunk by sentences or large punctuation
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    current_chunk = ""
    for s in sentences:
        s = s.strip()
        if not s: continue
        current_chunk += s + " "
        if len(current_chunk) > 100:  # ~100 chars per chunk
            kb_chunks.append({"source": "index.html", "text": current_chunk.strip()})
            current_chunk = ""
    if current_chunk:
        kb_chunks.append({"source": "index.html", "text": current_chunk.strip()})
        
except Exception as e:
    print("Error parsing HTML:", e)

# 2. Parse PDFs
pdfs = glob.glob('*.pdf')
for p in pdfs:
    try:
        doc = fitz.open(p)
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text").strip()
            if text:
                text = re.sub(r'\s+', ' ', text)
                sentences = re.split(r'(?<=[.!?]) +', text)
                current_chunk = ""
                for s in sentences:
                    s = s.strip()
                    if not s: continue
                    current_chunk += s + " "
                    if len(current_chunk) > 100:
                        kb_chunks.append({"source": p, "text": current_chunk.strip()})
                        current_chunk = ""
                if current_chunk:
                    kb_chunks.append({"source": p, "text": current_chunk.strip()})
    except Exception as e:
        print(f"Error parsing PDF {p}:", e)

# 3. Add some hardcoded facts that are crucial (addresses, people)
# This ensures it always gets the most critical facts right if the scraper missed the context.
kb_chunks.append({"source": "manual", "text": "(주)비에이텍의 본사 및 공장은 강원특별자치도 춘천시 퇴계공단2길 64에 위치해 있습니다. 전화번호는 033-264-9243, 팩스는 033-251-5747, 이메일은 gwf0123@hanmail.com 입니다."})
kb_chunks.append({"source": "manual", "text": "비에이텍의 대표이사는 조세연입니다. 조직은 생산부, 관리부, 품질보증부로 나뉩니다."})
kb_chunks.append({"source": "manual", "text": "비에이텍은 부스터 펌프 시스템, 산업용 펌프(벌류트, 수중, 오수, 슬러지 등)를 제조 및 판매합니다."})

# 4. Generate JS file
js_content = "const knowledgeBase = " + json.dumps(kb_chunks, ensure_ascii=False, indent=4) + ";"
with open("knowledge_base.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Generated knowledge_base.js with {len(kb_chunks)} chunks.")
