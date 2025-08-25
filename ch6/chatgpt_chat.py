import openai
# 클라이언트 생성 
client = openai.OpenAI()
# 대화 이력을 유지하는 변수 ---- (1)
messages = []
# API를 호출하는 함수         ---- (2)
def call_chatgpt_chat(user_text):
    # 대화 이력에 사용자의 입력을 추가 ---- (3)
    messages.append({'role': 'user', 'content': user_text})
    # AP를 호출 ---- (4)
    completion = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=messages)
    #대화 이력을 추가 ---- (5) 
    res = completion.choices[0].message.content
    messages.append({'role': 'assistant', 'content': res})
    return res
# 사용자가 입력한 내용을 연속으로 질문 ---- (6)
while True:
    user = input('YOU: ')
    # 대화를 종료?
    if user == 'quit' or user == 'exit':
        break
    if user == '': continue
    # 챗GPT를 호출한다 ---- (7)
    res = call_chatgpt_chat(user)
    print('AI: ' + res)