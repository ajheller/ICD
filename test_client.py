from zero import ZeroClient

zero_client = ZeroClient("localhost", 5559)


def echo():
    resp = zero_client.call("echo", "Hi there!")
    print(resp)


def hello():
    resp = zero_client.call("hello_world", None)
    print(resp)


def initialize():
    resp = zero_client.call("initialize", None)
    print(resp)


def run():
    resp = zero_client.call("run", None)
    print(resp)
    return resp


def get_status():
    resp = zero_client.call("status", None)
    print(resp)
    return resp


if __name__ == "__main__":
    initialize()
    get_status()
    run()
    get_status()
    echo()
    hello()
