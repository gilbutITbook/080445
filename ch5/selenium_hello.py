from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
# WebDriver 초기화 
driver = webdriver.Chrome()
# Google 홈페이지를 연다 
driver.get("https://www.google.com")
# 검색 박스를 찾아 키워드를 입력한다 
search_box = driver.find_element("name", "q")
search_box.send_keys("자동 제어 테스트")
# Enter 키를 눌러 검색을 시작한다
search_box.send_keys(Keys.RETURN)
# 페이지거 로드되는 것을 기다린다(최대 5초 대기)
driver.implicitly_wait(5)
# 5초 대기 
time.sleep(5)
# 브라우저를 닫는다 
driver.quit()