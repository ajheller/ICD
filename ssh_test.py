from fabric import Connection
import time

HOST = "pi" #"192.168.2.2"
USER = "heller"


def update(n=10):
    with Connection(HOST, USER) as conn:
        for i in range(n):
            result = conn.run("date; sleep 1", hide=True)
            result = conn.run("date >> log.txt", hide=True)
            print(result.stdout, time.time())
