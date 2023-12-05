from rpc_client import RPCClient
if __name__ == "__main__":
    rpc_client = RPCClient()
    rpc_client.connect()
    rpc_client.start_consuming()
