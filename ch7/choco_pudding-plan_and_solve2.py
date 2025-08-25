import plan_and_solve, json, time
# 질문을 지정 --- (*1)
question = '''
가게에서 320원인 푸딩과 210원인 초콜릿을 여러 개 사고 1만 원을 지불했습니다.  
거스름돈은 450원이었습니다. 초콜릿과 푸딩을 각각 몇 개씩 샀을까요?  
결과는 아래와 같이 JSON 형식으로 출력하세요.
`{"초콜릿": 초콜릿 수량, "푸딩": 푸딩 수량}`
'''.strip()

# 초기 질문을 별도 변수로 보관
original_question = question
failure_history = []  # 실패 사례 누적 저장

# 최대 횟수를 지정하여 답을 얻는다 --- (*2)
success = False
for attempt in range(1,11):
    print(f'\n=== 시도 {attempt}/5 ===')
     # 누적된 실패 사례를 포함한 프롬프트 생성 
    current_prompt = original_question
    if failure_history:
        current_prompt += "\n### 실패 사례 기록:\n" + "\n".join(failure_history)

    result, response = plan_and_solve.plan_and_solve(current_prompt)
    try:
        # 결과를 검산한다 --- (*3)
        result = result.replace("'", '"') # 문자열의 인용부호를 조정
        o = json.loads(result)
        print('결과:', o)
        total = o['푸딩'] * 320 + o['초콜릿'] * 210
        if total == (10000 - 450):
            print('=== 정답 ===')
            success = True
            break
        else:
            print(f'유감입니다. 계산 금액: {total}원 (목표: 9550원)')
            # 틀린 경우 실패 사례를 누적 --- (*4) 
            failure_history.append(
                f"시도 {attempt} 실패:\n응답:\n{response}\n계산: {total}원"
            )
    except Exception as e:
        print('[ERROR] JSON형식 데이터가 출력되지 않았습니다.\n', e)
    time.sleep(7)
    
if not success:
    print('\n=== 종료 ===\n시행회수가 제한 회수를 넘었습니다.')
