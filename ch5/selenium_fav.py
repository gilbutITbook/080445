import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# WebDriver 초기화
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # 1. 로그인
    driver.get("https://uta.pw/sakusibbs/users.php?action=login")
    driver.find_element(By.ID, "user").send_keys("book-prompt")
    driver.find_element(By.ID, "pass").send_keys("1LUSwKxrsc6WKk1y")
    driver.find_element(By.CSS_SELECTOR, "#loginForm input[type=submit]").click()
    time.sleep(1)

    # 2. 작품 목록 페이지 이동
    driver.get("https://uta.pw/sakusibbs/users.php?user_id=1")
    time.sleep(1)

    # 3. 작품 링크 수집
    ul = driver.find_element(By.CSS_SELECTOR, "#mmlist")
    url_list = [a.get_attribute("href") for a in ul.find_elements(By.TAG_NAME, "a")]

    # 4. 각 작품 페이지에서 즐겨찾기 버튼 클릭
    for url in url_list:
        driver.get(url)
        time.sleep(1)
        fav_button = driver.find_elements(By.CSS_SELECTOR, "#fav_add_btn")
        if fav_button:
            fav_button[0].click()
            time.sleep(1)

finally:
    driver.quit()
