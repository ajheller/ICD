from my_client import RpcClient, zero_client

client = RpcClient(zero_client)

if __name__ == "__main__":
    client.echo("Hi there!")
    client.hello_world(None)
