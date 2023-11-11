# import tkinter as tk
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 크롬 드라이버 경로 설정
driver_path = './chromedriver.exe'

# 크롬 옵션 생성
chrome_options = Options()
chrome_options.add_argument('--ignore-proxy-server')

# 크롬 브라우저 열기
driver = webdriver.Chrome(driver_path)

# 네이버 사이트 접속
driver.get('https://www.daum.net')

# 원하는 동작 수행

# 브라우저 종료
driver.quit()


# # def search_product():
# # search_query = entry.get()

#     # 크롬 브라우저를 사용하여 네이버 쇼핑 사이트 열기
# header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
# url = 'https://www.naver.com'
# driver = webdriver.Chrome('./chromedriver.exe')
# driver.get(url)

#     try:
#         # 검색창에 입력된 상품명 검색
#         search_input = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '#autocompleteWrapper input[name="query"]'))
#         )
#         search_input.send_keys(search_query)
#         search_input.submit()

#         # 상품 정보 가져오기
#         product_name = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '._model_list .basicList_title__3P9Q7 a'))
#         ).text
#         product_price = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '._model_list .basicList_price__2r23_ em'))
#         ).text
#         review_count = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '._model_list .basicList_etc_box__1Jzg6 a:nth-child(3)'))
#         ).text

#         # 결과 출력
#         result_label.config(text=f'상품명: {product_name}\n가격: {product_price}\n리뷰 수: {review_count}')

#     except Exception as e:
#         result_label.config(text=f'오류 발생: {str(e)}')

#     finally:
#         driver.quit()


# # GUI 생성
# root = tk.Tk()
# root.title('네이버 쇼핑 크롤러')

# label = tk.Label(root, text='상품 검색:')
# label.pack()

# entry = tk.Entry(root)
# entry.pack()

# search_button = tk.Button(root, text='검색', command=search_product)
# search_button.pack()

# result_label = tk.Label(root, text='', wraplength=400)
# result_label.pack()

# root.mainloop()
