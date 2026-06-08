import re

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

if '<script src="knowledge_base.js"></script>' not in html:
    html = html.replace('<script src="main.js"></script>', '<script src="knowledge_base.js"></script>\n    <script src="main.js"></script>')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

# 2. Update main.js
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

old_getai_pattern = re.compile(r'function getAIResponse\(query\) \{.*?\return "죄송합니다.*?\}', re.DOTALL)

new_getai = """function getAIResponse(query) {
            const q = query.replace(/\\s+/g, '');
            if (/안녕|반가워|하이/.test(q)) {
                return "안녕하세요! 저는 비에이텍의 펌프 시스템과 기술에 대해 안내해 드리는 AI 도우미입니다. 무엇을 도와드릴까요?";
            }
            
            if (typeof knowledgeBase === 'undefined') {
                return "지식 베이스 데이터베이스를 불러오지 못했습니다.";
            }
            
            const tokens = query.split(/\\s+/).filter(t => t.length > 0);
            
            let bestChunk = null;
            let maxScore = 0;
            
            for (const chunk of knowledgeBase) {
                let score = 0;
                const text = chunk.text.toLowerCase();
                for (const token of tokens) {
                    if (text.includes(token.toLowerCase())) {
                        score += token.length;
                    }
                }
                
                if (score > maxScore) {
                    maxScore = score;
                    bestChunk = chunk;
                }
            }
            
            if (maxScore > 0 && bestChunk) {
                let sourceLabel = "";
                if(bestChunk.source === "index.html") sourceLabel = "[웹사이트 문서]";
                else if(bestChunk.source === "manual") sourceLabel = "[기본 정보]";
                else sourceLabel = `[자료: ${bestChunk.source}]`;
                
                return `해당 내용에 대해 찾은 결과입니다:\\n\\n"${bestChunk.text}"\\n\\n출처: ${sourceLabel}`;
            }

            return "죄송합니다. 현재 내부 문서와 웹사이트 정보에서 질문하신 내용에 대한 답변을 찾지 못했습니다. 다른 검색어나 키워드로 질문해 주시겠어요?";
        }"""

match = old_getai_pattern.search(js)
if match:
    js = js.replace(match.group(0), new_getai)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)

print("RAG Logic injected successfully.")
