import openai, time, json

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

# 도구를 선택하는 프롬프트를 실행 --- (*3)
def select_tool(prompt):
    # 프롬프트를 실행 
    prompt = prompt.replace('`', '"') # `를 에스케이프
    st_prompt = SELECT_TOOL_TEMPLATE.replace('{input}', prompt)
    res = call_chatgpt(st_prompt)
    print('=== 응답 ===\n' + res)
    try:
        # JSON을 가져오기 --- (*4)
        if '```json' in res:
            res = res.split('```json')[1].split('```')[0]
        # 문자열을 JSON으로 변환 --- (*4a)
        data = json.loads(res)
        action = data['행동']
        arg = data['인수']
        memo = data['비고']
        # 언어 모델이 선택한 도구에 따라 처리한다 --- (*5)
        if action == '계산기':
            val = eval(arg)
            return f'{memo}→{val}' # 인수를 계산해서 반환한다
        elif action == '검색':
            return f'{arg}를 검색합니다(TODO)' + memo
        elif action == '현재시각':
            return time.strftime('%Y년%m월%d일 %H:%M') + '→' + memo
        else:
            return '도구를 찾을 수 없습니다.' + res
    except Exception as e:
        return 'JSON을 가져올 수 없습니다.' + e

# 메인처리 --- (*6)
if __name__ == '__main__':
    prompt = '4300원인 감을 30상자, 3000인 딸기를 50상자 샀어. 모두 얼마일까?'
    res = select_tool(prompt)
    print('=== 결과 ===\n' + res)

