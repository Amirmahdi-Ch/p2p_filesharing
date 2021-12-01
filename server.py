import uvicorn
from fastapi import FastAPI
import client
import threading

for f in client.friend_nodes:
    print(f)

app = FastAPI()


def run_server():
    if __name__ == "__main__":
        uvicorn.run(app, host="localhost", port=client.port_number, access_log=False, log_level="critical")


def read_request():
    while (True):
        input_str = input()
        x = input_str.split()
        if x[0] == "request":
            print("request")
        else:
            print("command not found")


t1 = threading.Thread(target=run_server)
t2 = threading.Thread(target=read_request)

t1.start()
t2.start()

t1.join()
t2.join()


@app.get("/file")
def getfile(filename: str):
    return filename
