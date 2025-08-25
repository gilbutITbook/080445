import openai, json, wikipediaapi, re
import chromadb_summarize as summarize
# 검색 키워드를 얻기 위한 프롬프트 템플릿 --- (*1)
SEARCH_KEYWORD_TEMPLATE = '''
### 지시:
다음 질문에 답하기 위해 Wikipedia를 검색할거야.
답변에 필요한 정보 페이지 제목을 몇 개 나열해줘.
### 질문:
```{question}```
### 출력형식:
JSON형식으로 출력해.
```json
["제목1", "제목2", "제목3"]
```
'''
# 질문에 답하기 위한 프롬프트 템플릿 --- (*2)
QA_TEMPLATE = '''
### 지시:
다음 정보를 참고로 해서 질문에 대답해.
또한, 중간 경과를 하나씩 열거하면서 질문의 답을 생각해줘.
### 정보:
```{info}```
### 질문:
```{question}```
'''

def extract_json_from_result(text):
    match = re.search(r'\[\s*["\'].*?["\']\s*(?:,\s*["\'].*?["\']\s*)*\]', text, re.DOTALL)
    if match:
        return match.group(0)
    else:
        raise ValueError("JSON 리스트가 result에서 발견되지 않았습니다.")

# 질문을 수행하는 함수 --- (*3)
def ask_question(question):
    # 검색 키워드를 결정한다 --- (*4)
    question = question.replace('`', '"') # 에스케이프
    prompt = SEARCH_KEYWORD_TEMPLATE.format(question=question)
    result = summarize.call_chatgpt(prompt)

    try:
        json_text = extract_json_from_result(result)
        title_list = json.loads(json_text)
    except Exception as e:
        print("JSON 파싱 오류:", e)
        title_list = []

    print('=== 검색 키워드 ===\n', title_list)
    
    # 기사를 가져와서 DB에 저장 --- (*5)
    for title in title_list:
        text = summarize.get_wikitext(title)
        summarize.insert_text(f'{title}: {text}')
    # 질문과 관계가 있어 보이는 텍스트 가져오기 --- (*6)
    info = summarize.query_text(question)
    # 질문에 답한다 --- (*7)
    prompt = QA_TEMPLATE.format(info=info, question=question)
    print('=== 질문 프롬프트 ===\n', prompt)
    result = summarize.call_chatgpt(prompt)
    print('=== 응답 ===\n', result)
   
    return result

if __name__ == '__main__':
    # 실제로 질문한다 --- (*8)
    question = '달이 지구에 미치는 영향을 알려줘.'
    ask_question(question)
