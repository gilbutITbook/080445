import itertools
# 주어진 4개의 수 
numbers = [1, 2, 9, 3]
# 가능한 모든 숫자 순열 
permutations = list(itertools.permutations(numbers))
# 모든 연산자 조합
operators = ['+', '-', '*', '/']
operator_combinations = list(itertools.product(operators, repeat=3))
# 모둔 수와 연산자의 조합을 테스트
for perm in permutations:
    for ops in operator_combinations:
        a, b, c, d = perm
        op1, op2, op3 = ops
        # 계산식 작성 
        expression = f"({a} {op1} {b}) {op2} ({c} {op3} {d})"
        try:
            # 계산하고 결과가 24와 같은지 체크
            result = eval(expression)
            if result == 24:
                print(f"계산식: {expression} = 24")
                exit()
        except ZeroDivisionError:
            continue
print("24를 만드는 계산식을 찾지 못했습니다.")