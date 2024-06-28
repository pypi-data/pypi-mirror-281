import argparse
from terminalbot.bot import get_message, send_message

def main():
    parser = argparse.ArgumentParser(description="Send and receive messages from a Telegram group")
    parser.add_argument('--token', required=True, help='Telegram bot token')
    parser.add_argument('--id', required=True, help='Telegram group chat ID')
    parser.add_argument('--message', help='Message to send to the group')
    parser.add_argument('--message-receive', help='Message to send after receiving a message')

    args = parser.parse_args()

    if args.message:
        send_message(args.token, args.id, args.message)
        print("Your message sent to the Telegram group")
    else:
        message = get_message(args.token, args.id)
        if message:
            print(message)
            if args.message_receive:
                send_message(args.token, args.id, args.message_receive)

if __name__ == '__main__':
    main()
