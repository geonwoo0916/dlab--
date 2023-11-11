from bs4 import BeautifulSoup
import requests

# 사이트 URL
url = "https://orbi.kr/list/tag/%EC%9E%85%EC%8B%9C%EC%9E%90%EB%A3%8C,%EC%B6%94%EC%B2%9C"

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
    if "정시" in title :
        print("[중요] 정시대비정보")
    elif "수능" in title:
        print("[중요] 수능대비정보")
    elif "수시" in title :
        print("수시대비정보")
    elif "컴공" in title :
        print("*컴공대비정보")
    print("제목:", title)
    print("내용:", content)
    print("댓글수:", comment)
    print("-----------")