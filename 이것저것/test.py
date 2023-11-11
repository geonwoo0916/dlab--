import time

# 1초마다 숫자 출력
def Time(num):
    n = num
    print(n)
    for i in range(0, num):
        n -= 1
        time.sleep(1)
    print(n)
Time(5)