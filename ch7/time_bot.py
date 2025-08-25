import openai, time

# ChatGPT의 API를 호출하는 함수 --- (*1)
def call_chatgpt(prompt):
    # API를 호출한다 
    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}])
    # 응답을 반환 
    return completion.choices[0].message.content

# 사용자로부터 질문을 입력한다 --- (*2)
user = input('무엇을 물어볼까요?>')
user = user.replace('`', '"') # `를 에스케이프 

# 현재 시간을 반환하는 프롬프트를 작성 --- (*3)
datetime_str = time.strftime('%Y년%m월%d일일 %H:%M')
prompt = f'''
### 지시:
다음 전제 정보를 이용해서 질문에 답해줘.
### 전제 정보:
현재 시작: {datetime_str}
### 질문 답변 예시:
- 질문: 지금 몇시입니까?
- 답변: 지금은 {datetime_str}입니다。
### 질문:
```{user}```
'''

# ChatGPT를 호출한다 --- (*4)
res = call_chatgpt(prompt)
print('AI의 답변: ' + res)

