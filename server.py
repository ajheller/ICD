from zero import ZeroServer

STATUS_SUCCESS = 0
STATUS_FAIL = 1

state_store = {"running": False}

app = ZeroServer(port=5559)


@app.register_rpc
def echo(msg: str) -> str:
    return msg


@app.register_rpc
async def hello_world() -> str:
    return "hello world"


@app.register_rpc
def initialize() -> int:
    return STATUS_SUCCESS


@app.register_rpc
def status() -> bool:
    print("server", state_store["running"])
    return state_store["running"]


@app.register_rpc
def run() -> int:
    state_store["running"] = True
    return STATUS_SUCCESS


@app.register_rpc
def get_state_store() -> dict:
    return state_store


if __name__ == "__main__":
    app.run(1)
