def sieve_of_eratosthenes(limit):
    # 초기화
    primes = [True] * (limit + 1)
    primes[0] = primes[1] = False

    # 에라스토테네스의 체 실행
    for current in range(2, int(limit**0.5) + 1):
        if primes[current]:
            for multiple in range(current * current, limit + 1, current):
                primes[multiple] = False

    # 결과 수집 
    prime_numbers = [num for num, is_prime in enumerate(primes) if is_prime]
 
    return prime_numbers

limit = 100
prime_numbers = sieve_of_eratosthenes(limit)

# 출력 결과 
print("100 이하의 소수는 다음과 같습니다:")
print(prime_numbers)