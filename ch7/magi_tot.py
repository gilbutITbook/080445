# MAGI ToT를 이용해서 질문에 답하는 프로그램 
import openai, time
# OpenAI 클라이언트 생성하기  
client = openai.OpenAI()
max_tokens = 250 # API를 여러 번 호출하므로 짧게 설정
# 역할을 지정하여 챗GPT를 호출하는 함수 --- (*1)
def gen_text(role, prompt, model='gpt-3.5-turbo'):
    system_msg = {'role': 'system', 'content': role}
    user_msg = {'role': 'user', 'content': prompt}
    response = client.chat.completions.create(
        model=model, max_tokens=max_tokens,
        temperature=0.8,
        messages=[system_msg, user_msg])
    time.sleep(0.5)
    return response.choices[0].message.content.strip()

# API를 사용해 MAGI ToT를 구현하는 함수 --- (*2)
def magi_tot(roles, question):
    print(f'=== 아래 질문에응답합니다  ===\n{question}')
    # 전문가 한 사람씩 질문한다 --- (*2a)
    answers = []
    for role in roles:
        role_p = f'당신은 {role}의 대표입니다.' + \
            f'질문을 진지하게 받아들이고, {role}다운 의견을 진술합니다.'
        answer = gen_text(role_p, question)
        print(f'=== 역할: {role} ===\n{answer}')
        answers.append([role, answer])
    # 전문가의 대답을 종합한 답을 출력한다 --- (*2b)
    summary = magi_summarize(question, answers)
    # (*2a)と(*2b)를 바탕으로 전문가의 의견을 구한다 --- (*2c)
    prompt2 = \
        '### 지시:\n우선 아래 질문에 대한 답변에 대해서 찬성이나 반대로 의견을 진술하세요.\n' + \
        f'### 질문:\n{question}\n' + \
        f'### 답변:\n{summary}\n' + \
        '### 출력예:\n- 찬성 or 반대: 이곳에 이유\n'
    print(f'=== 전문가에게 다시 질문합니다 ===\n{prompt2}')
    answers = []
    for role in roles:
        role_p = f'당신은 {role}의 대표입니다. 건설적이고 솔직한 의견을 진술합니다.'
        answer = gen_text(role_p, prompt2)
        print(f'=== 역할: {role} ===\n{answer}')
        answers.append([role, answer])
    # 다시 전문가의 의견을 종합한다 --- (*2d)
    summary = magi_summarize(question, answers)
    return summary

# 전문가의 의견을 종합하는 함수 --- (*3)
def magi_summarize(question, answers):
    answer_prompt = '\n'.join([
        f'### 전문가 ({role})의 의견:\n{a}' for role, a in answers])
    summary_prompt = \
        '### 지시:\n아래 질문에 답하세요.\n' + \
        '단 아래 전문가들의 의견을 요약해서 간결한 결론과 이유를 제출하세요.\n' + \
        f'### 질문:\n{question}\n' + \
        answer_prompt
    print('=== 통합용 프롬프트 ===\n' + summary_prompt)
    summary = gen_text(
        '당신은 선량하고 공평한 재판관입니다. 전문가의 의견을 바탕으로 결론을 내립니다.', 
        summary_prompt)
    print('=== 위 의견을 종합한 것 ===\n' + summary)
    return summary

if __name__ == '__main__': # 메인 처리 --- (*4)
    question = \
        '사무직 3대 남성이 점심을 먹습니다.' + \
        '오늘 추천할 만한 메뉴를 제안해 주세요.' + \
        '간단하게 메뉴와 그 이유를 한마디로 답해주세요.'
    roles = ['영양사', '애정이 넘치는 어머니', '젊은 여성']
    magi_tot(roles, question)
