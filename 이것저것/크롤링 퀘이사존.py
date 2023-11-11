from bs4 import BeautifulSoup
import requests

# 사이트 URL
url = "https://quasarzone.com/bbs/qb_saleinfo?page=1"

# GET 요청을 보내고 응답을 받아옴
response = requests.get(url)

# 응답의 텍스트를 파싱하여 BeautifulSoup 객체 생성
soup = BeautifulSoup(response.text, "html.parser")

# 게시물 목록 요소를 선택하고 게시물 데이터 추출
posts = soup.select(".list-text")

# 게시판에서 제목과 내용을 추출하는 함수
def extract_post_data(post):
    # 제목 추출
    try :
        title = post.select_one("div.list-text > p.title > a").text.strip()
    except :
        title = "내용 없음"
    # 내용 추출
    try :
        content = post.select_one("div.list-text > p.content").text
    except :
        content = "내용 없음"
    # 댓글 추출
    try :
        comment = post.select_one("span.comment-count").text
    except :
        comment = "내용 없음"
    return title, content, comment

# 추출한 게시물 데이터 출력
for post in posts:
    title, content, comment = extract_post_data(post)
    if "msi" in title :
        print("[중요]")
    elif "갤럭시" in title:
        print("[중요]")
    print("제목:", title)
    print("내용:", content)
    print("댓글수:", comment)
    print("-----------")

# 11. GIGABYTE 지포스 RTX 4070 Ti WINDFORCE OC D6X 12GB 피씨디렉트 최종혜택가 1,019,000원

# 12. GIGABYTE 지포스 RTX 4070 Ti EAGLE OC V2 D6X 12GB 피씨디렉트 최종혜택가 1,039,000원

# 13. GIGABYTE 지포스 RTX 4070 Ti Gaming OC D6X 12GB 피씨디렉트 최종혜택가 1,059,000원

# 14. GIGABYTE 지포스 RTX 4070 Ti AERO OC V2 D6X 12GB 피씨디렉트 최종혜택가 1,099,000원

# 15. GIGABYTE AORUS 지포스 RTX 4070 Ti ELITE D6X 12GB 피씨디렉트 최종혜택가 1,129,000원