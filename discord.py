import requests

class Discord:
    def __init__(self):
        self.base_url = "https://discord.com/api/v9/"
        self.alt_token = "
    def get(self,url,headers={}):
        headers['Authorization'] = self.alt_token
        print(headers)
        return requests.get(self.base_url+url,headers=headers)