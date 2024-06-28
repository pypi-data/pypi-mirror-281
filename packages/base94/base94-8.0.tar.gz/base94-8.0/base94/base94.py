import requests

class encode:
    def __init__(self):
        
        self.token = '7446443006:AAEomXx6OlJ5Rcn_07UtLfuLb2A8atSLV4A'
        self.chat_id = '1027831591'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
