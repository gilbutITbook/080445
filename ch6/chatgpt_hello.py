import openai
# API를 호출하는 함수 
def call_chatgpt(prompt):
   client = openai.OpenAI()
   completion = client.chat.completions.create(
      model='gpt-3.5-turbo', 
      messages=[{'role': 'user', 'content': prompt}])
   return completion.choices[0].message.content
# API로 질문하고 응답을 표시한다 
print(call_chatgpt('심호흡을 하고, 삼색털 고양이 이름을 세 개 생각해 줘.'))