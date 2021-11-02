import requests
key = "KUKI6N6bX2Wgd"
def tkuki(msg):
    Kuki = requests.get(f"https://www.kukiapi.xyz/api/apikey={key}/emiko/@race_up/message={msg}]").json()

    kreply = f"{Kuki['reply']}"

    return kreply
