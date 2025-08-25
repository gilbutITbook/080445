def get_prime(num):
    if num < 2:
        return []
    
    primes = []
    for i in range(2, num + 1):
        is_prime = True
        for j in range(2, int(i ** 0.5) + 1):
            if divmod(i, j)[1] == 0:  # 나머지 확인
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    
    return primes

# 테스트 실행
print(get_prime(30))
