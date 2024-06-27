import requests
import sys
import time

class TelegramBot:
    def __init__(self, bot_token, group_chat_id):
        self.bot_token = bot_token
        self.group_chat_id = group_chat_id
        self.api_url = f'https://api.telegram.org/bot{bot_token}/'
        self.last_update_id = None

    def get_updates(self):
        params = {'timeout': 100, 'offset': self.last_update_id}
        response = requests.get(self.api_url + 'getUpdates', params=params)
        if response.status_code == 200:
            return response.json()
        else:
            if __name__ == '__main__':
                print(f"Failed to get updates: {response.text}")
            return None

    def get_message(self):
        updates = self.get_updates()
        if updates and 'result' in updates:
            for update in updates['result']:
                self.last_update_id = update['update_id'] + 1
                if 'message' in update and 'text' in update['message']:
                    return update['message']['text']
        return None

    def send_message(self, text):
        params = {'chat_id': self.group_chat_id, 'text': text}
        response = requests.post(self.api_url + 'sendMessage', params=params)
        if response.status_code != 200:
            if __name__ == '__main__':
                print(f"Failed to send message: {response.text}")

def get_message(bot_token, group_chat_id):
    bot = TelegramBot(bot_token, group_chat_id)
    return bot.get_message()

def send_message(bot_token, group_chat_id, message):
    bot = TelegramBot(bot_token, group_chat_id)
    bot.send_message(message)

def main():
    if len(sys.argv) < 3:
        print("Usage: terminalbot <bot_token> <group_chat_id> [--after_message <after_message>]")
        sys.exit(1)
    
    bot_token = sys.argv[1]
    group_chat_id = sys.argv[2]
    after_message = None

    if '--after_message' in sys.argv:
        after_message_index = sys.argv.index('--after_message') + 1
        if after_message_index < len(sys.argv):
            after_message = sys.argv[after_message_index]
    
    bot = TelegramBot(bot_token, group_chat_id)

    while True:
        message = bot.get_message()
        if message:
            print(f"Message received: {message}")
            if message.lower() == "stop terminalbot":
                print("Stopping bot.")
                break
            if after_message:
                bot.send_message(after_message)
                print(f"Sent message: {after_message}")
        time.sleep(1)

if __name__ == '__main__':
    main()
