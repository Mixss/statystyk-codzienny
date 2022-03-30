import json


def set_default_channel(server_id, channel_id):
    with open("data/config.json") as file:
        data = json.load(file)
    #check if config contains this server
    contains = False
    for el in data["BroadcastChannels"]:
        if el["ServerId"] == server_id:
            el["ChannelId"] = channel_id
            contains = True
            break
    if not contains:
        data["BroadcastChannels"].append({
            "ServerId": server_id,
            "ChannelId": channel_id
        })
    with open("data/config.json", "w") as f:
        json.dump(data, f)


def get_channels():
    with open("data/config.json") as file:
        data = json.load(file)

    return data["BroadcastChannels"]
