from rpc_client import RPCClient
from model import LitModel
import time


if __name__ == "__main__":
    model = LitModel()
    rpc_client = RPCClient(model)
    while True:
        try:
            rpc_client.connect()
            rpc_client.start_consuming()
        except Exception as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            time.sleep(3)