import argparse

import requests

DEFAULT_SERVER = "http://localhost:8080"


def register(server: str, user_id: str, name: str, device_id: str) -> None:
    """Register a new user with the server."""
    url = f"{server}/api/users/register"
    payload = {"userId": user_id, "name": name, "deviceId": device_id}
    resp = requests.post(url, json=payload, timeout=5)
    resp.raise_for_status()
    print(resp.text)


def send_message(server: str, sender: str, receiver: str, message: str) -> None:
    """Send a message from sender to receiver."""
    url = f"{server}/api/send"
    payload = {"sender": sender, "receiver": receiver, "message": message}
    resp = requests.post(url, json=payload, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    print(f"Status: {data.get('status')} - ID: {data.get('message_id')}")


def receive_messages(server: str) -> None:
    """Retrieve stored messages from the server."""
    url = f"{server}/api/receive"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    for msg in data.get("messages", []):
        ts = msg.get("timestamp")
        sender = msg.get("sender")
        content = msg.get("message")
        mid = msg.get("id")
        print(f"[{ts}] {sender}: {content} (ID: {mid})")


def ack_message(server: str, message_id: str) -> None:
    """Acknowledge delivery of a message."""
    url = f"{server}/api/messages/ack"
    resp = requests.post(url, params={"messageId": message_id}, timeout=5)
    resp.raise_for_status()
    print(f"Acknowledged {message_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple chat client")
    parser.add_argument("--server", default=DEFAULT_SERVER, help="Server base URL")
    subparsers = parser.add_subparsers(dest="command", required=True)

    reg = subparsers.add_parser("register", help="Register a new user")
    reg.add_argument("--user-id", required=True)
    reg.add_argument("--name", required=True)
    reg.add_argument("--device-id", required=True)

    snd = subparsers.add_parser("send", help="Send a message")
    snd.add_argument("--sender", required=True)
    snd.add_argument("--receiver", required=True)
    snd.add_argument("--message", required=True)

    rcv = subparsers.add_parser("receive", help="Receive messages")

    ack = subparsers.add_parser("ack", help="Acknowledge a message")
    ack.add_argument("--message-id", required=True)

    args = parser.parse_args()

    if args.command == "register":
        register(args.server, args.user_id, args.name, args.device_id)
    elif args.command == "send":
        send_message(args.server, args.sender, args.receiver, args.message)
    elif args.command == "receive":
        receive_messages(args.server)
    elif args.command == "ack":
        ack_message(args.server, args.message_id)
