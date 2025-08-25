import openai, os
# API를 호출하는 함수                                     --- (1)
def call_chatgpt(prompt):
      # Azure설정을 읽들인다(환경 변수에 설정을 적어 둔다)       --- (2)
      client = openai.AzureOpenAI()
      # API를 호출한다                                   --- (3) 
      completion = client.chat.completions.create(
            model='test-gpt-4o-mini', # 3a
            messages=[{'role': 'user', 'content': prompt}])
      return completion.choices[0].message.content
# 실제로 동작한다                                           -- (4)
print(call_chatgpt('오늘 점심에 먹고 싶은 음식과 그 이유를 말해줘. '))
