# 계획과 해결 프롬프트(Plan-and-Solve)로 문제를 해결한다 
import openai
import subprocess, sys

# 계획과 해결 프롬프트(Plan-and-Solve) 템플릿 --- (*1)
PS_PROMPT = '''
### 지시:
아래 질문에 대해 다음 단계에 따라 생각해 주세요.
### 단계:
1. 문제를 정리한다.
2. 문제를 해결할 계획을 세운다.
3. 위 단계를 바탕으로 Python 프로그램만 작성한다.
### 질문:
{question}
### 출력형식:
1. 문제 정리: [문제 분석]
2. 계획: [해결 계획]
3. 프로그램: 
```python
# 여기에 Python 코드
```
'''.strip()

# OpenAI 클라이언트 설정 --- (*2)
max_tokens = 800 # 프로그램 코드를 생성받기 위해 크게 설정
api_mode = 'openai' # or 'azure'
azure_model = 'test-gpt-35-turbo'

# ChatGPT를 호출하는 함수 --- (*3)
def gen_text(prompt, model='gpt-3.5-turbo'):
    sys_msg = {
        'role': 'system', 
        'content': 'You are an intelligent and diligent systems engineer.' + \
            'You analyze problems accurately and create programs.'}
    user_msg = {'role': 'user', 'content': prompt}
    # OpenAi인지 Azure인지에 따라 API선택 --- (*3a)
    if api_mode == 'azure':
        client = openai.AzureOpenAI()
        model = azure_model
    else:
        client = openai.OpenAI() 
    response = client.chat.completions.create(
        model=model, max_tokens=max_tokens,
        temperature=0.9,
        messages=[sys_msg, user_msg])
    return response.choices[0].message.content.strip()

# Python 코드를 파일에 저정하고 실행한다 --- (*4)
def save_and_run(py):
    tempfile = '_temp.py'
    with open(tempfile, 'wt', encoding='utf-8') as f:
        f.write(py)
    cmd = [sys.executable, tempfile]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

# 문제를 해결하는 함수 --- (*5)
def plan_and_solve(question):
    # 프롬프트를 만들어 대규모 언어 모델을 호출한다 --- (*6)
    prompt = PS_PROMPT.format(question=question)
    print('=== 프롬프트 ===\n' + prompt)
    res = gen_text(prompt)
    print('=== 응답 ===\n' + res)
    # 응답에서 프로그램을 추출 --- (*7)
    if '```python' in res:
        # 프로그램 실행 --- (*8)
        try:
          py = res.split('```python\n')[1].split('```')[0].strip()
          #print('\n=== 프로그램 ===\n' + py)
          result = save_and_run(py)
          if result.strip():
            print('\n=== 실행 결과 ===\n' + result.strip())
          else:
            print('\n[INFO] 실행 결과가 없습니다.')
          return result, res
        except Exception as e:
          print('[ERROR] 코드 실행 실패:', e)
        #  return '', res
    else:
        print('\n=== 설명 ===\n프로그램 코드가 생성되지 않았습니다.')
        return '', res

if __name__ == '__main__': # 메인처리 --- (*9)
    question = '''
A와 B 두 개의 양초가 있습니다.
각각 불을 붙이면 1분간 1.25cm씩 짧아집니다.
A는 20cm인데, 동시에 불을 붙이고 B가 2/3가 탔을 때 A는 다 타버렸습니다.
B 양초의 길이와 다 타는데 걸리는 시간을 계산하세요.
아래 JSON 형식(ensure_ascii=False)으로 답을 출력하세요.
{"B의 길이": "답 cm", "B가 다 타는 시간": "답 분"} 
### 힌트: 
불을 붙이고 A의 길이가 0cm가 되었을 때, B는 2/3가 탔습니다.
즉, B의 길이는 A의 3/2이며, 전부 연소되는 시간도 3/2배입니다.
'''.strip()
    plan_and_solve(question)
