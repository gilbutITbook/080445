import magi_tot
# 질문
question = '''
자가 소유가 나을까요, 아니면 전세나 월세가 나을까요?  
최대한 간결하게, 답변과 그 이유를 제시하세요.  
가족 구성: 30대 부부, 자녀 2명  
세대 연소득: 약 5,000만 원  
거주 지역: 서울 근교
'''.strip()
# 전문가를 지정 
roles = ['부동산 전문가', '경영 컨설턴트', '현명한 어머니']
magi_tot.max_tokens = 350 # 조금 길게 설정
# 토론 시작 
magi_tot.magi_tot(roles, question)
