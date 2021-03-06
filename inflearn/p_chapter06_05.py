# Chapter06-05
# Fatures 동시성
# 비동기 작업 실행
# 지연시간(Block) CPC 및 리소스 낭비 방지 -> (File)Network I/O관련 잡업
# -> 동시성 활용 권장
# 비동기 작업과 적합한 프로그램일 경우 압도적으로 성능 향상

# futures : 비동기 실행을 위한 API를 고수준으로 작성 -> 사용하기 쉽도록 개선
# concurrent.futures
# 1. 멀티스레딩/멀티프로세싱 API 통일 -> 매우 사용하기 쉬움
# 2. 실행중인 작업 취소, 완료 여부 체크, 타임아웃 옵션, 콜백추가, 동기화 코드
#    매우 쉽게 작성 -> promise 개념

# 2가지 패턴 실습
# concurrent.futures map
# concurrent.futures wait, as_completed

# GIL(Global interpreter lock)
#  : 두 개 이상의 스레드가 동시에 실행 될 때 하나의 자원을 엑세스 하는 경우
#   -> 문제점을 방지하기 위해 GIL 실행, 리소스 전체에 락이 걸린다.
#   -> context switch(문맥 교환)


# GIL : 멀티프로세싱 사용, cPython


import os
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait, as_completed

WORK_LIST = [10000, 100000, 1000000, 10000000]

# 동시성 합계 계산 메인 함수
# 누적 함계 함수(제네레이터)

def sum_generator(n):
    return sum(n for n in range(1, n+1)) 

# wait
# as_completed
def main():
    # Worker Count
    worker = min(10, len(WORK_LIST))

    # 시작 시간
    start_time = time.time()
    # futures
    futures_list = []

    # 결과 건수
    # ProcessPoolExcuotor
    with ProcessPoolExecutor() as excutor:
        for work in WORK_LIST:
            # future 반환
            future = excutor.submit(sum_generator, work)
            print('future-->',future)
            # 스케줄링
            futures_list.append(future)
            # 스케줄링 확인
            print('Scheduled for {} : {}'.format(work, future)) # Scheduled for 10000 : <Future at 0x2060d434340 state=running>...
            print()
        # # wait 결과 출력
        # result = wait(futures_list, timeout=7)
        # # 성공
        # print('Completed Tasks : ' + str(result.done))
        # # 실패
        # print('Pending ones after waiting for 7seconds : ' + str(result.not_done))
        # # 결과 값 출력
        # print([future.result() for future in result.done])

        # as_completed 결과 출력 
        for future in as_completed(futures_list): # futures_list = [<Future at 0x2060d434340 state=running>....]
            result = future.result()
            # future = <Future at 0x21ca73d3430 state=finished returned int>
            # future.result = <bound method Future.result of <Future at 0x191af4b2460 state=finished returned int>>
            # future.result() = 50005000
            done = future.done()
            cancelled = future.cancelled

            # future 결과 확인
            print("Future Result : {}, Done : {}".format(result, done))
            print("Future Cancelled : {}".format(cancelled))





    # 종료 시간
    end_time = time.time() - start_time
    # 출력 포멧
    msg = '\n Time : {:.2f}s'
    # 최종 결과 출력
    print(msg.format(end_time))



# 실행
if __name__ == '__main__':
    main()


"""
future.result = <bound method Future.result of <Future at 0x191af4b2460 state=finished returned int>>
클래스는 여러 멤버 함수들을 포함할 수 있다. 이 멤버 함수들은 공통적으로 'self'를 첫 번째 입력 인자를 가진다. 
이것은 이 함수가 어떤 클래스에 속해 있는 method라는 것을 의미한다. 이것을 bound method라고 한다. 

출처: https://gmnam.tistory.com/226 [Voyager]
"""