import requests

class Baxi_API:
    def __init__(self, api_key):
        self.api_key = api_key

    def create_welcome_banner(self, background_url, text1, text2, profile_pic_url):
        url = 'http://api.pyropixle.com/v1/create-banner'
        data = {
            "background_url": background_url,
            "text1": text1,
            "text2": text2,
            "profile_pic_url": profile_pic_url,
            "api_key": self.api_key
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return str(response.json()["image_url"])
        else:
            return str(response.json()["error"])
        
    def get_chatfilter_event(self, request_id):
        url = 'http://api.pyropixle.com/v1/chatfilter_event_data'
        data = {
            "request_id": request_id,
            "api_key": self.api_key
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return str(response.json())
        else:
            return str(response.json()["error"])