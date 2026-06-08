import fitz
import glob
pdfs = glob.glob('*Prompt*.pdf')
if not pdfs:
    print("No Prompt PDF found")
else:
    doc = fitz.open(pdfs[0])
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    print(text[:1000]) # Print first 1000 chars to see what it looks like
