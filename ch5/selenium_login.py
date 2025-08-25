from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# ChromeDriver 자동 설치 및 브라우저 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 로그인
driver.get("https://uta.pw/sakusibbs/users.php?action=login")
driver.find_element(By.CSS_SELECTOR, "#user").send_keys("book-prompt")
driver.find_element(By.CSS_SELECTOR, "#pass").send_keys("1LUSwKxrsc6WKk1y")
driver.find_element(By.CSS_SELECTOR, "#loginForm input[type=submit]").click()

# 마이페이지 이동
driver.get("https://uta.pw/sakusibbs/users.php?user_id=2045")

# 링크 클릭
driver.find_element(By.LINK_TEXT, "一覧をCSVでダウンロード").click()

# 잠시 대기 후 종료
time.sleep(3)
driver.quit()
