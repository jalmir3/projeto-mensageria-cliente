#!/usr/bin/env python3
import requests
import time
import sys
from datetime import datetime

SERVER_URL = "http://localhost:8080/api"  # Confirme esta URL conforme seu servidor


def test_connection():
    """Testa se o servidor está funcionando usando o endpoint /receive"""
    try:
        response = requests.get(f"{SERVER_URL}/receive")
        if response.status_code == 200:
            print("✅ Conexão com o servidor estabelecida com sucesso!")
            return True
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
            print(f"✅ Mensagem enviada! ID: {data.get('message_id', 'N/A')}")
            return True
        print(f"❌ Erro ao enviar: {response.status_code} - {response.text}")
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
                print(f"\n📬 Mensagens recebidas ({data.get('count', 0)}):")
                for msg in messages:
                    # Converte timestamp de milissegundos para segundos
                    timestamp = datetime.fromtimestamp(msg['timestamp'] / 1000).strftime('%H:%M:%S')
                    print(f"  [{timestamp}] {msg.get('sender', 'Anônimo')}: {msg.get('message', '')}")
            else:
                print("📭 Nenhuma mensagem nova")
            return True
        print(f"❌ Erro ao receber: {response.status_code} - {response.text}")
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
    print("\n💬 Modo interativo - Digite suas mensagens (digite 'sair' para parar)")

    # Pedir nome do usuário
    sender = input("Seu nome: ").strip() or "Anônimo"
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


def print_help():
    print("\nUso:")
    print("  python message_client.py test          # Testa conexão")
    print("  python message_client.py send          # Modo interativo para enviar")
    print("  python message_client.py receive       # Recebe mensagens uma vez")
    print("  python message_client.py monitor       # Monitora mensagens continuamente")
    print("  python message_client.py help          # Mostra esta ajuda")


def main():
    if len(sys.argv) < 2 or sys.argv[1].lower() == 'help':
        print("🚀 Cliente de Mensagens - Compatível com Servidor Java")
        print("-" * 45)
        print_help()
        return

    command = sys.argv[1].lower()

    print("\n🚀 Cliente de Mensagens - Compatível com Servidor Java")
    print("-" * 45)

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
        print_help()


if __name__ == "__main__":
    main()