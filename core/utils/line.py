import requests


def send(token, message, img_url=None):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {token}",
    }
    data = {"message": message, }
    if img_url is not None:
        data["imageThumbnail"] = img_url
        data["imageFullsize"] = img_url
    response = requests.post(url, headers=headers, data=data)
    try:
        response.raise_for_status()
    except requests.RequestException:
        pass
