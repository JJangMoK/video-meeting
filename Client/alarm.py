import threading
from threading import Lock
import time

"""
1. 함수를 등록
함수는 특정 값이 바뀌면 예외를 던지게 한다.
2. 시간을 지정
시간(초)를 지정하고 start라는 함수를 실행한 이후로
시간이 모두 지나면 특정 값을 바꾸어 함수가 예외를 던지게 함
"""


class _Alarm:
    """
    1. register the function call back.
    Alarm has a condition variable makes call back function
    to throw Exception
    2. set timer (sec)
    method start(sec) will wait for sec to run out and
    changes the condition variable to call back function to
    throw Exception
    """
    def __init__(self, func, sec):
        self.func = func
        self.stop = True
        self.lock = Lock()
        self.sec = sec
        self.waiter = None

    def __start(self):
        self.lock.acquire()
        if self.stop and not self.waiter:
            self.stop = False
            self.lock.release()
            self.waiter = threading.Thread(target=self.__wait, daemon=True)
            self.waiter.start()
            return
        self.lock.release()

    def __wait(self):
        time.sleep(self.sec)
        with self.lock:
            self.stop = True

    def __call__(self, *args, **kwargs):
        self.__start()
        with self.lock:
            if self.stop:
                self.waiter = None
                raise Exception("time out")
        self.func(*args, **kwargs)


def Alarm(func=None, sec=0):
    def wrapper(func):
        return _Alarm(func, sec)
    return wrapper
