#!/usr/bin/env python3
import requests
import time
import sys

SERVER_URL = "http://localhost:8080/api"


def test_connection():
    """Testa se o servidor está funcionando"""
    try:
        response = requests.get(f"{SERVER_URL}/test")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['message']}")
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False


def send_message(message, sender="Anônimo"):
    """Envia uma mensagem para o servidor"""
    try:
        payload = {
            "message": message,
            "sender": sender
        }
        response = requests.post(f"{SERVER_URL}/send", json=payload)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['message']}")
            return True
        else:
            print(f"❌ Erro ao enviar: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def receive_messages():
    """Recebe mensagens do servidor"""
    try:
        response = requests.get(f"{SERVER_URL}/receive")

        if response.status_code == 200:
            data = response.json()
            messages = data['messages']

            if messages:
                print(f"\n📬 Recebidas {len(messages)} mensagem(s):")
                for msg in messages:
                    timestamp = time.strftime('%H:%M:%S', time.localtime(msg['timestamp'] / 1000))
                    print(f"  [{timestamp}] {msg['sender']}: {msg['message']}")
            else:
                print("📭 Nenhuma mensagem nova")
            return True
        else:
            print(f"❌ Erro ao receber: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def monitor_messages():
    """Monitora mensagens continuamente"""
    print("🔄 Monitorando mensagens... (Ctrl+C para parar)")
    try:
        while True:
            receive_messages()
            time.sleep(2)  # Verifica a cada 2 segundos
    except KeyboardInterrupt:
        print("\n👋 Parando monitoramento...")


def interactive_mode():
    """Modo interativo para enviar mensagens"""
    print("💬 Modo interativo - Digite suas mensagens (digite 'sair' para parar)")

    # Pedir nome do usuário
    sender = input("Seu nome: ").strip()
    if not sender:
        sender = "Anônimo"

    print(f"Olá {sender}! Comece a digitar suas mensagens:")

    while True:
        try:
            message = input(f"{sender}> ").strip()

            if message.lower() in ['sair', 'exit', 'quit']:
                print("👋 Tchau!")
                break

            if message:
                send_message(message, sender)

        except KeyboardInterrupt:
            print("\n👋 Tchau!")
            break


def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python simple_client.py test          # Testa conexão")
        print("  python simple_client.py send          # Modo interativo para enviar")
        print("  python simple_client.py receive       # Recebe mensagens uma vez")
        print("  python simple_client.py monitor       # Monitora mensagens continuamente")
        return

    command = sys.argv[1].lower()

    print("🚀 Cliente de Mensagens Simples")
    print("-" * 30)

    if command == "test":
        test_connection()

    elif command == "send":
        if test_connection():
            interactive_mode()

    elif command == "receive":
        if test_connection():
            receive_messages()

    elif command == "monitor":
        if test_connection():
            monitor_messages()

    else:
        print(f"❌ Comando desconhecido: {command}")


if __name__ == "__main__":
    main()