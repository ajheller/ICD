# learning condition variables

import threading as th
import time


def consumer(cv):
    while True:
        with cv:
            print("C - waiting")
            cv.wait()
            print("C doing")
        time.sleep(0.1)
    print("C exiting")


def producer(cv):
    print("p")
    for i in range(10):
        print("P notifying", i)
        with cv:
            cv.notify_all()
        time.sleep(0.5)


cv = th.Condition()

ct = th.Thread(target=consumer, args=(cv,))

ct.start()

producer(cv)
