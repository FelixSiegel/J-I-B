import json
# try to load necessary variables of bot -> if Error close script
try:
    with open("./data/server_datas.json", "r") as sI:
        servers: dict = json.load(sI)

except Exception as e:
    print(f"\n\033[91m[ERROR]:\033[00m Error occurred on loading JSON-File with the server datas.\nError-Code: {e}\n")
    # if cant loaded
    exit()
guild_ids = [servers[server]["id"] for server in servers]  # server ids