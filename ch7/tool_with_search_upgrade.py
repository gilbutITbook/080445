import os, openai, time, json, wikipediaapi

# 도구 선택 프롬프트 템플릿 --- (*1)
SELECT_TOOL_TEMPLATE = """
### 지시:
주어진 도구 목록에서 적절한 도구를 선택하고, 목표를 달성해 주세요.
### 도구 목록:
- 검색: 지정한 키워드를 Wikipedia에서 검색합니다.
  - 인수:
    - 키워드: 검색 키워드
- 현재 시간: 현재 시각을 반환합니다.
- 계산기: 지정한 계산식을 계산합니다.
  - 인수:
    - 계산식: 예) 3 * (4 + 5)
### 목표:
```{input}```
### 출력 예시:
다음과 같은 형식으로 JSON으로 출력하세요.
```json
{"행동": "도구 이름", "인수": "여기에 인수", "비고": "여기에 비고"}
```
"""

# ChatGPT 호출 함수 --- (*2)
def call_chatgpt(prompt):
    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}])
    return completion.choices[0].message.content.strip()

# JSON 데이터 파싱 함수 --- (*3)
def get_json_data(response):
    if '```json' in response:
        response = response.split('```json')[1].split('```')[0]
    try:
        return json.loads(response)
    except Exception as e:
        print('JSON 파싱 실패:', e)
        return {}

# GPT에게 키워드 3개 추천 요청 --- (*4)
def generate_search_keywords(question):
    prompt = f"""
### 지시:
다음 질문을 Wikipedia에서 검색할 경우 가장 적절한 검색 키워드 3개를 추천해 주세요.
사람 이름, 직책, 개념, 목록 등을 포함해 주세요.
한 줄에 하나씩 출력해 주세요.

질문: "{question}"
"""
    keywords = call_chatgpt(prompt).split('\n')
    return [k.strip() for k in keywords if k.strip()]

# 여러 키워드를 Wikipedia에서 요약 --- (*5)
def get_multiple_wikipedia_summaries(keywords):
    wiki = wikipediaapi.Wikipedia('llm-wiki-search', 'ko')
    summaries = []
    for keyword in keywords:
        #print(f'=== 검색: {keyword} ===')
        print(f'wikipedia.page= {keyword}')  
        page = wiki.page(keyword)
        if page.exists():
            print(page.summary[:1000])
            summaries.append(f'[{keyword}]\n{page.summary[:1000]}\n')
        else:
            print('검색 결과가 없습니다.')
            summaries.append(f'[{keyword}]\n검색 결과가 없습니다.\n')
    return "\n\n".join(summaries)

# 검색 도구 실행 --- (*6)
def search_tool(question):
    keywords = generate_search_keywords(question)
    summary = get_multiple_wikipedia_summaries(keywords)
    prompt = f"""### 지시:
아래 정보를 참고하여 질문에 대답해 주세요.
### 정보:
{summary}
### 질문:
{question}
"""
    print('=== 응답 프롬프트 ===')
    print(prompt)
    return call_chatgpt(prompt)

# 도구 선택 및 실행 --- (*7)
def selec_tool(question):
    question = question.replace('`', '"')  # 백틱 이스케이프
    st_prompt = SELECT_TOOL_TEMPLATE.replace('{input}', question)
    print('=== 도구 선택 프롬프트 ===\n' + st_prompt)
    res = call_chatgpt(st_prompt)
    print('=== 도구 선택 응답 ===\n' + res)
    data = get_json_data(res)
    action = data.get('행동')
    arg = data.get('인수')
    memo = data.get('비고')
    
    if action == '계산기':
        val = eval(arg)
        return f'=== 계산기 ===\n{memo} → {val}'
    elif action == '현재 시간':
        return time.strftime('%Y년 %m월 %d일 %H:%M') + ' → ' + memo
    elif action == '검색':
        return search_tool(question)
    else:
        return '적절한 도구를 찾을 수 없습니다.\n' + res

# 메인 처리 --- (*8)
if __name__ == '__main__':
    prompt = '현재 대한민국 대통령은 누구야?'
    res = selec_tool(prompt)
    print('=== 결과 ===\n' + res)
