import argparse
from .bot import get_message, send_message

def main():
    parser = argparse.ArgumentParser(description="Interact with a Telegram group.")
    parser.add_argument('bot_token', type=str, help='The bot token.')
    parser.add_argument('group_chat_id', type=str, help='The group chat ID.')
    parser.add_argument('--message', type=str, help='The message to send.')
    parser.add_argument('--message-receive', type=str, help='The message to send automatically after receiving a message.')

    args = parser.parse_args()

    if args.message:
        send_message(args.bot_token, args.group_chat_id, args.message)
        return

    message = get_message(args.bot_token, args.group_chat_id)
    if message and args.message_receive:
        send_message(args.bot_token, args.group_chat_id, args.message_receive)

if __name__ == '__main__':
    main()
