#!/usr/bin/env python3
import requests
import websocket
import threading
import json
from datetime import datetime

SERVER_URL = "http://localhost:8080/api"
WEBSOCKET_URL = "ws://localhost:8080/ws/messages"


class HttpClient:
    def __init__(self, sender, recipient):
        self.sender = sender
        self.recipient = recipient

    def send_message(self, message):
        payload = {
            "sender": self.sender,
            "recipient": self.recipient,
            "message": message
        }
        try:
            response = requests.post(f"{SERVER_URL}/send-to", json=payload)
            if response.status_code == 200:
                print(f"Enviado via HTTP! ID: {response.json().get('message_id')}")
            else:
                print(f"HTTP erro: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Erro HTTP: {e}")

    def receive_messages(self):
        try:
            response = requests.get(f"{SERVER_URL}/receive/{self.recipient}")
            if response.status_code == 200:
                messages = response.json()
                if not messages:
                    print("📭 Nenhuma mensagem.")
                for msg in messages:
                    timestamp = datetime.fromtimestamp(msg['timestamp'] / 1000).strftime('%H:%M:%S')
                    print(f"[{timestamp}] {msg['sender']} → {msg['recipient']}: {msg['message']}")
            else:
                print(f"HTTP erro: {response.status_code}")
        except Exception as e:
            print(f"Erro ao receber via HTTP: {e}")


def on_message(ws, message):
    try:
        data = json.loads(message)
        timestamp = datetime.fromtimestamp(data['timestamp'] / 1000).strftime('%H:%M:%S')
        print(f"[{timestamp}]{data.get('sender')} → {data.get('recipient')}: {data.get('message')}")
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")


def on_close(ws, code, msg):
    print("Conexão WebSocket encerrada.")


def on_error(ws, error):
    print(f"Erro WebSocket: {error}")


class WebSocketClient:
    def __init__(self, sender, recipient):
        self.sender = sender
        self.recipient = recipient

    def on_open(self, ws):
        print("Conexão WebSocket aberta!")

        def send_loop():
            while True:
                msg = input(f"{self.sender}> ")
                if msg.lower() in ['sair', 'exit']:
                    ws.close()
                    break
                payload = {
                    "sender": self.sender,
                    "recipient": self.recipient,
                    "message": msg
                }
                ws.send(json.dumps(payload))

        threading.Thread(target=send_loop).start()

    def connect(self):
        ws = websocket.WebSocketApp(
            f"{WEBSOCKET_URL}?user={self.sender}",
            on_message=on_message,
            on_open=self.on_open,
            on_close=on_close,
            on_error=on_error
        )
        ws.run_forever()


def menu_http(sender, recipient):
    client = HttpClient(sender, recipient)

    while True:
        print("\nModo HTTP")
        print("1. Enviar mensagem")
        print("2. Receber mensagens")
        print("3. Sair")
        choice = input("Escolha: ").strip()

        if choice == "1":
            msg = input(f"{sender}> ")
            client.send_message(msg)
        elif choice == "2":
            client.receive_messages()
        elif choice == "3":
            print("Saindo do modo HTTP")
            break
        else:
            print("Opção inválida")


def menu_websocket(sender, recipient):
    client = WebSocketClient(sender, recipient)
    client.connect()


def main():
    print("Cliente de Mensagens")
    print("1. Usar HTTP")
    print("2. Usar WebSocket")
    mode = input("Escolha o modo (1 ou 2): ").strip()

    sender = input("Seu nome: ").strip()
    recipient = input("Destinatário: ").strip()

    if mode == "1":
        menu_http(sender, recipient)
    elif mode == "2":
        menu_websocket(sender, recipient)
    else:
        print("Modo inválido.")


if __name__ == "__main__":
    main()
