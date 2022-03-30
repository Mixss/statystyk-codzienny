import json

def set_default_channel(server_id, message_id):
    with open("data/config.json") as file:
        data = json.load(file)
    data[server_id] = message_id
    with open("data/config.json", "w") as f:
        json.dump(data, f)
