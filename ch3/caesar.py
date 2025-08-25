def caesar_cipher(text, shift):
    encrypted_text = ""
    for char in text:
        # 문자가 알파벳인 경우만 암호화합니다.
        if char.isalpha():
            # 문자가 대문자인지 소문자인지 확인하고 알파벳 범위 내에서 시프트합니다.
            if char.isupper():
                encrypted_char = chr(((ord(char) - 65 + shift) % 26) + 65)
            else:
        encrypted_char = chr(((ord(char) - 97 + shift) % 26) + 97)
        else:
            # 알파벳이 아닌 문자는 변경하지 않고 그대로 추가합니다.
            encrypted_char = char
        encrypted_text += encrypted_char
    return encrypted_text

# 테스트용 문자열과 시프트 값을 설정합니다.
text = "Hello, World!"
shift = 3
# 텍스트를 카이사르 암호로 암호화합니다.
encrypted_text = caesar_cipher(text, shift)
print("암호화된 문자열:", encrypted_text)