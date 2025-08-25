from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 1. 드라이버 초기화 및 창 최대화
driver = webdriver.Chrome()  # 조건에 맞게 설정
driver.maximize_window()

# 2. 첫 번째 페이지로 이동 및 캡처
driver.get('https://www.gilbut.co.kr/')
time.sleep(2)  # 페이지 로딩 대기
driver.save_screenshot('web1.png')

# 3. 두 번째 페이지로 이동 및 캡처
driver.get(' https://kujirahand.com/)
time.sleep(2)  # 페이지 로딩 대기
driver.save_screenshot('web2.png')

# 드라이버 종료
driver.quit()
