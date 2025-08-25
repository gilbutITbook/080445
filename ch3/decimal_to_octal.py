def decimal_to_octal(n):
    # n이 0이하인 경우 그대로 반환한다 
    if n <= 0:
        return '0'
 
    octal_result = ''
 
    while n > 0:
        # n을 8로 나눈 나머지를 m으로 한다
        m = n % 8
        # n을 8로 나눈 몫을 새로운 n으로 한다 
        n = n // 8
        # m을 결과 맨 앞에 추가한다
        octal_result = str(m) + octal_result
 
    return octal_result

# 테스트 
decimal_value = 42 # 10진수 값 
octal_value = decimal_to_octal(decimal_value)
print(f"{decimal_value}의 8진수 표현은 {octal_value}입니다.")