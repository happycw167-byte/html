with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix broken alt texts
html = html.replace('alt="입형, 볼루트펌프 성능시험설비">용접기(제조사 : 아세아(주))">', 'alt="전기 용접기(제조사 : 아세아(주))">')
html = html.replace('alt="성능시험용 유량계">절단기(제조사 : 아세아(주))">', 'alt="프라즈마 절단기(제조사 : 아세아(주))">')
html = html.replace('alt="2.8ton 크레인">(제조사 : (주)삼성호이스트)">', 'alt="호이스트 크레인(제조사 : (주)삼성호이스트)">')
html = html.replace('alt="20ton 천정크레인">\n                    </div>\n                    <div class="equipment-info">\n                        <h3>공장 외부 전경</h3>', 'alt="공장 외부 전경">\n                    </div>\n                    <div class="equipment-info">\n                        <h3>공장 외부 전경</h3>')
html = html.replace('alt="부스터펌프 성능시험설비">\n                    </div>\n                    <div class="equipment-info">\n                        <h3>성능시험장</h3>', 'alt="성능시험장">\n                    </div>\n                    <div class="equipment-info">\n                        <h3>성능시험장</h3>')
html = html.replace('alt="수중펌프 성능시험설비">\n                    </div>\n                    <div class="equipment-info">\n                        <h3>펌프 출고대기소</h3>', 'alt="펌프 출고대기소">\n                    </div>\n                    <div class="equipment-info">\n                        <h3>펌프 출고대기소</h3>')

# Also, I messed up the images for item 1, 4, 6 because my multi_replace was aggressive.
# Let's fix those factory_img tags
html = html.replace("openCertModal('factory_img_13.jpeg')", "openCertModal('factory_img_1.jpeg')").replace('src="factory_img_13.jpeg" alt="공장 외부 전경"', 'src="factory_img_1.jpeg" alt="공장 외부 전경"')
html = html.replace("openCertModal('factory_img_10.jpeg')", "openCertModal('factory_img_4.jpeg')").replace('src="factory_img_10.jpeg" alt="성능시험장"', 'src="factory_img_4.jpeg" alt="성능시험장"')
html = html.replace("openCertModal('factory_img_9.jpeg')", "openCertModal('factory_img_6.jpeg')").replace('src="factory_img_9.jpeg" alt="펌프 출고대기소"', 'src="factory_img_6.jpeg" alt="펌프 출고대기소"')

# Wait, the easiest way is to re-read the clean index.html from a backup if it exists, or just fix it.
# Let's write the fixed html back.
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
