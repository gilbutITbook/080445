import os, openai, time, json, wikipediaapi
# 도구를 선택하는 프롬프트 --- (*1)
SELECT_TOOL_TEMPLATE = '''
### 지시:
주어진 도구 목록에서 어울리는 도구를 선택하고, 목표를 달성하기 위해 노력할 것.
### 도구 목록:
- 계산기: 인수로 제공한 계산식을 계산한다.
 - 인수:
 - 계산식: 계산식을 지정 
- 검색: 지정한 키워드를 검색한다.
 - 인수:
 - 키워드: 검색 키워드 
- 현재 시간: 현재 시간을 반환한다.
### 목표:
```{input}```
### 출력 형식:
JSON형식으로 출력한다.
```json
{"행동": "도구 이름", "인수": "여기에 인수", "비고": "여기에 비고"}
```
'''

# ChatGPT API를 호출하는 함수 --- (*2)
def call_chatgpt(prompt):
    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}])
    return completion.choices[0].message.content
    

# JSON 데이터를 가져온다 --- (*3)
def get_json_data(response):
    if '```json' in response:
        response = response.split('```json')[1].split('```')[0]
    try:
        return json.loads(response)
    except Exception as e:
        print('JSON을 가져올 수 없습니다.' + e)
    return ''


def generate_search_keywords(question):
    prompt = f"""
### 지시:
다음 질문을 Wikipedia에서 검색하려고 합니다. 적절한 **검색 키워드 5개**를 추천해 주세요.
- 사람 이름, 개념, 직책, 관련 문서 제목, 목록 등으로 구성해 주세요.
- 한 줄에 하나씩, 중복 없이, 설명 없이 출력해 주세요.
- 최소한 키워드 하나는 공백 없는 단일 단어로 추천해줘.

질문: "{question}"
"""
    keywords = call_chatgpt(prompt).split('\n')
    return [k.strip() for k in keywords if k.strip()]

# Wikipedia API를 호출해서 검색 결과를 반환한다 --- (*4)
def get_wikipedia(arg):
    wiki = wikipediaapi.Wikipedia('llm-wiki-search', 'ko')
    page_name = arg.strip().replace(' ', '_')

    print('wikipedia.page=', page_name)

    fname = f"wikipedia_cache_{page_name}.txt"
    if os.path.exists(fname):
        try:
            return open(fname, "r", encoding="utf-8").read()
        except UnicodeDecodeError:
            return open(fname, "r", encoding="cp949").read()

    page = wiki.page(page_name)
    if page.exists():
        summary = f'- {arg}: {page.summary}\n'
        with open(fname, "w", encoding="utf-8") as f:
            f.write(summary)
        return summary
    else:
        return f'[{arg}] 페이지를 찾을 수 없습니다.'


# 검색 도구를 이용했을 때의 처리 --- (*5)
def search_tool(question, _arg=None):
    keywords = generate_search_keywords(question)
    summaries = []

    for keyword in keywords:
        print(f'=== 검색: {keyword} ===')
        summary = get_wikipedia(keyword)
        print(summary)
        summaries.append(f"[{keyword}]\n{summary.strip()}")

    full_summary = "\n\n".join(summaries)
    prompt = (
        "### 지시:\n"
        "아래 정보를 참고해서 질문에 정확하게 대답해줘.\n"
        "### 정보:\n"
        f"{full_summary}\n"
        "### 질문:\n"
        f"{question}\n"
    )
    print("=== 응답 프롬프트 ===")
    print(prompt)
    return call_chatgpt(prompt)

# 도구를 선택하는 프롬프트를 실행 --- (*6)
def select_tool(question):
    # 프롬프트 실행
    question = question.replace('`', '"') # `를 에스케이프 
    st_prompt = SELECT_TOOL_TEMPLATE.replace('{input}', question)
    print('=== 행동 선택 프롬프트 ===\n' + st_prompt)
    res = call_chatgpt(st_prompt)
    print('=== 응답 ===\n' + res)
    data = get_json_data(res)
    action = data['행동']
    arg = data['인수']
    memo = data['비고']
    # 언어 모델이 선택한 도구에 따라 처리한다 --- (*7)
    if action == '계산기':
        val = eval(arg) # 인수를 계산 
        return f'=== 계산기 ===\n{memo} → {val}'
    elif action == '현재 시간':
        return time.strftime('%Y년%m월%d일 %H:%M') + '→' + memo
    elif action == '검색':
        return search_tool(question, arg)
    else:
        return '도구를 찾을 수 없습니다.' + res

# 메인처리 --- (*8)
if __name__ == '__main__':
    prompt = '2025년 대한민국 대통령은 누구야?'
    res = select_tool(prompt)
    print('=== 결과 ===\n' + res)
