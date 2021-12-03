import uvicorn
from fastapi import FastAPI
import util
import threading
from fastapi.responses import FileResponse
import requests
from os import getcwd
from fastapi.responses import FileResponse

# for f in util.friend_nodes:
#     print(f)

app = FastAPI()


@app.get("/file", response_class=FileResponse)
def getfile(file_name: str):
    return FileResponse(path=f"./{util.owned_files_dir}/{file_name}",
                        media_type="text", status_code=200)

def checkSeen(node, seenNodes):
    for seen in seenNodes:
        if int(seen) == node:
            return True
    return False

@app.get("/port")
def getfile(file_name: str, seen: str):
    friendNodes = []
    seenNodes = seen.split(",")
    fileFound = False

    for i in range(len(util.friend_nodes)):
        friendNodes.append(util.friend_nodes[i].copy())

    for ownedFile in util.owned_files:
        if ownedFile == file_name:
            # return FileResponse(path=f"./{util.owned_files_dir}/{file_name}",
            #                     media_type="text", status_code=200)
            print(type(util.port_number))
            seenNew = seen + "," + str(util.node_number)
            return (f'{str(util.port_number)}|{seenNew}')

    # if len(friendNodes) == 1 and friendNodes[0]["node_name"] == parent and not fileFound:
        # return FileResponse(path="NOT_FOUND.txt", media_type="text", status_code=200)
        # return -1
    cnt = len(friendNodes)
    for friend in friendNodes:
        if checkSeen(friend["node_name"], seenNodes):
            cnt -= 1
    if cnt == 0:
        seenNew = seen + "," + str(util.node_number)
        return (f'-1|{seenNew}')

    for ownFriend in friendNodes:
        print(f'http://localhost:{ownFriend["node_port"]}/port')

        if checkSeen(ownFriend["node_name"], seenNodes):
            continue

        seenNew = seen + "," + str(util.node_number)
        f = requests.get(f'http://localhost:{ownFriend["node_port"]}/port',
                         params={"file_name": file_name, "seen": seenNew})

        # if f.content.decode('ascii') != "-1":
        #     break
        f = f.text[1:(len(f.text) - 1)]
        print(f)
        if f.split("|")[0] != '-1':
            print("break")
            break

    return f


# @router.get("/file")
# def get_file(name_file: str):
#    return FileResponse(path=getcwd() + "/" + name_file)

def run_server():
    if __name__ == "__main__":
        uvicorn.run(app, host="localhost", port=util.port_number, access_log=False)


def read_request():
    while (True):
        input_str = input()
        x = input_str.split()

        if x[0] == "request":
            print("request")
            fileRequested = x[1]
        else:
            print("command not found")
            continue

        fileFound = False
        for ownFile in util.owned_files:
            if (ownFile == fileRequested):
                fileFound = True
                print(f"GET FILE FROM NODE {util.node_number}")

        if not fileFound:
            for ownFriends in util.friend_nodes:
                port = requests.get(f"http://localhost:{ownFriends['node_port']}/port",
                                    params={"file_name": fileRequested,
                                    "parent": util.node_number, "seen":str(util.node_number)})

                # if f.content.decode('ascii') != "-1":
                #     break
                port = port.text[1:(len(port.text) - 1)]
                if port.split("|")[0] != '-1':
                    print(f"A file found {port}")
                    break

            print(port)
            f = requests.get(f"http://localhost:{port.split('|')[0]}/file",
                             params={"file_name": fileRequested})
            fw = open(f"./{util.new_files_dir}/{fileRequested}", "wb")
            fw.write(f.content)
            fw.close()


t1 = threading.Thread(target=run_server)
t2 = threading.Thread(target=read_request)

t1.start()
t2.start()

t1.join()
t2.join()