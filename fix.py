with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix layout for inquiry
bad_inq = '<div class="contact-layout mt-5" style="justify-content: center;">'
good_inq = '<div class="mt-5" style="display: flex; justify-content: center;">'
html = html.replace(bad_inq, good_inq)

# Fix layout for reference
start_idx = html.find('<!-- 3. 자료실 (Reference) -->')
if start_idx != -1:
    end_idx = html.find('<!-- 4. 고객지원 (Customer Support) -->', start_idx)
    ref_html = html[start_idx:end_idx]
    new_ref_html = ref_html.replace('col-md-6 mb-4', 'col-md-4 mb-4')
    html = html.replace(ref_html, new_ref_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
