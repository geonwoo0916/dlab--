import bardapi
import os

#바드 api 설치
#pip3 install bardapi

#api key를 입력하세요.
os.environ["_BARD_API_KEY"]="XwiTWzq0E8xSIVuXhoU4eEV_jIcWwrIlIMPXT2i4xnWzuMDXsAFU7ilhD-ZvZ3bvpI7Tjg."

#질문작성
input_text = "가수 성시경이 결혼을 했을까? 대답해봐."

#바드 대답
response = bardapi.core.Bard().get_answer(input_text)
for i, choice in enumerate(response['choices']): print(f"Choice {i+1}:Wn", choice['content'][0], "\n")