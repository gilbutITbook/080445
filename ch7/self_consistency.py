# 자기 일관성을 이용해서 올바른 나이를 구하는 프로그램
import openai, time
# 지금 해결할 문제를 지정 --- (*1)
QUESTION = '''
Q: 내가 8살 때 여동생은 내 나이의 절반이었다. 지금 나는 40살이다. 여동생은 몇 살일까?
A:
'''
# 문제 해결에 도움이 되는 힌트 --- (*2)
HINT = '''
Q: Q: 타로는 사탕 30개 중 절반을 여동생에게 줬어. 엄마는 사탕 10개를 여동생한테 줬어. 여동생은 사탕 몇 개 가지고 있을까?
A: 여동생은 타로한테서 30/2=15개 받았어. 엄마한테서 10개 더 받았으니까, 25개 가지고 있어. 답은 25개야.
Q: 타로는 닭 30마리, 지로는 닭 25마리를 키우고 있어. 해마다 한 마리씩 늘어나. 타로가 지금 닭을 40마리 키우고 있다면, 지로는 몇 마리일까?
A: 타로랑 지로의 닭 차이는 30-25=5마리야. 타로가 40마리 키운다는 건 40-30=10년 지난 거고, 지로도 그동안 매년 1마리씩 늘었을 테니까 25+10=35마리야. 답은 35마리야.
Q: 에리는 10살이야. 에리 아빠는 35살이야. 에리가 20살이 되면 아빠는 몇 살이야?
A: 에리랑 아빠랑 나이 차이는 35-10=15살이야. 에리가 20살 되면 20+15=35살이니까, 아빠도 35+10=45살이 되는 거야. 답은 45살이야.
Q: 큰 부자가 차를 30대 가지고 있어. 그 중 절반을 처분했는데, 그 뒤로 차를 5대 더 샀대. 그럼 지금 차 몇 대 가지고 있을까?
A: 원래 30대 중 절반을 팔았으니까 30/2=15대가 남았고, 거기에 5대 더 샀으니까 15+5=20대야. 답은 20대야.
'''
# 답을 도출하기 위한 프롬프트 --- (*3)
PROMPT_SELF_CONS = '''
### [지시]:
아래 질문에 대해 [전문가의 답변]을 통합해서 최종적인 결론과 이유를 제출해줘.
### [질문]:
{question}
### [전문가의 답변]:
{answers}
'''
# ChatGPT를 호출하는 함수 --- (*4)
def gen_text(prompt):
    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        max_tokens=250, # 답변을 짧게 한다 
        temperature=0.7,
        messages=[{'role': 'user', 'content': prompt}])
    time.sleep(1) # API 연속 호출을 방지하기 위해 1초 대기 --- (*4a)
    return completion.choices[0].message.content

# 자기 일관성을 이용하는 함수 --- (*5)
def self_consistency(question, hint, max_iter=3):
    # 임시 프롬프트를 구성성한다 --- (*6)
    prompt_q = \
        f'### Hint:\n{hint.strip()}\n' + \
        f'### Question:\n위 힌트를 참고로 생각해 줘. \n{question.strip()}'
    print(f'=== 임시 프롬프트 ===\n{prompt_q}')
    # 질문을 여러 번 반복 실행한다 --- (*7)
    answers = []
    for i in range(max_iter):
        answer = gen_text(prompt_q).replace('\n', '').strip()
        answers.append(answer)
        print(f'=== {i+1}회차 응답 ===\n{answer}')
    # 최종적인 답을 구하는 프롬프트를 구성한다 --- (*8)
    prompt_summary = PROMPT_SELF_CONS.format(
        question=question.strip(),
        answers='\n'.join([f'- (선택지{i+1}) {a}' for i, a in enumerate(answers)]))
    # 프롬프트를 실행해서 최종적인 답을 구한다 --- (*9)
    print(f'=== 최종적인 답을 얻는 프롬프트 ===\n{prompt_summary.strip()}')
    answer = gen_text(prompt_summary)
    return answer

if __name__ == '__main__': # 메인 처리 --- (*10)
    answer = self_consistency(QUESTION, HINT)
    print('=== 최종 답변 ===\n', answer)

