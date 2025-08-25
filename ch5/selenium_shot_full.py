import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 저장 폴더 설정
save_dir = "screenshots"
os.makedirs(save_dir, exist_ok=True)

# 헤드리스 크롬 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')  # 초기 창 크기

# 드라이버 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 전체 페이지 스크린샷 함수
def fullpage_screenshot(driver, file_path):
    w = driver.execute_script("return document.body.parentNode.scrollWidth")
    h = driver.execute_script("return document.body.parentNode.scrollHeight")
    driver.set_window_size(w, h)
    driver.save_screenshot(file_path)

# 캡처할 웹사이트 리스트
urls = [
    "https://www.gilbut.co.kr",
    "https://kujirahand.com"
]

# 현재 시간 (파일명용)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# 각 URL에 대해 스크린샷 찍기
for url in urls:
    driver.get(url)
    site_name = url.split("//")[1].split(".")[0]  # 예: gilbut, kujirahand
    filename = f"{site_name}_{timestamp}.png"
    filepath = os.path.join(save_dir, filename)
    fullpage_screenshot(driver, filepath)
    print(f"Saved screenshot: {filepath}")

# 드라이버 종료
driver.quit()
