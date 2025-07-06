#!/usr/bin/env python3
import requests
import sys
import time
from datetime import datetime

SERVER_URL = "http://localhost:8080/api"


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


def send_message_to(message, recipient, sender="Anônimo"):
    try:
        payload = {
            "message": message,
            "sender": sender,
            "recipient": recipient
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{SERVER_URL}/send-to", json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Mensagem enviada para {recipient}! ID: {data.get('message_id', 'N/A')}")
            return True
        print(f"❌ Erro ao enviar: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def receive_messages():
    """Recebe todas as mensagens do servidor"""
    try:
        response = requests.get(f"{SERVER_URL}/receive")

        if response.status_code == 200:
            messages = response.json()
            if messages:
                print(f"\n📬 Todas as mensagens ({len(messages)}):")
                for msg in messages:
                    timestamp = datetime.fromtimestamp(msg['timestamp'] / 1000).strftime('%H:%M:%S')
                    print(f"  [{timestamp}] De: {msg.get('sender', 'Anônimo')} Para: {msg.get('recipient', 'Todos')}: {msg.get('message', '')}")
            else:
                print("📭 Nenhuma mensagem disponível")
            return True
        print(f"❌ Erro ao receber: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def monitor_messages_for(recipient, interval=3):
    """Monitora novas mensagens para um destinatário específico"""
    print(f"\n🔔 Monitorando mensagens para {recipient} (Ctrl+C para parar)...")
    last_count = 0

    try:
        while True:
            response = requests.get(f"{SERVER_URL}/receive/{recipient}")

            if response.status_code == 200:
                messages = response.json()
                new_messages = messages[last_count:]  # Pega apenas as novas

                if new_messages:
                    print(f"\n📬 Novas mensagens para {recipient} ({len(new_messages)}):")
                    for msg in new_messages:
                        timestamp = datetime.fromtimestamp(msg['timestamp'] / 1000).strftime('%H:%M:%S')
                        print(f"  [{timestamp}] {msg.get('sender')}: {msg.get('message')}")
                    last_count = len(messages)
                else:
                    print(".", end="", flush=True)  # Indicador de atividade
            else:
                print(f"\n❌ Erro ao verificar mensagens: {response.status_code}")

            time.sleep(interval)  # Intervalo entre verificações

    except KeyboardInterrupt:
        print("\n👋 Parando monitoramento...")
    except Exception as e:
        print(f"\n❌ Erro fatal: {str(e)}")

def interactive_receive_mode():
    print("\nModo de recebimento - Escolha uma opção:")
    print("1. Ver todas as mensagens (uma vez)")
    print("2. Monitorar novas mensagens em tempo real")
    choice = input("Opção (1/2): ").strip()

    if choice == "1":
        receive_messages()
    elif choice == "2":
        recipient = input("Digite seu nome (destinatário): ").strip()
        if recipient:
            monitor_messages_for(recipient)
    else:
        print("❌ Opção inválida")


def interactive_send_mode():
    """Modo interativo para enviar mensagens"""
    print("\n💬 Modo de envio - Digite suas mensagens (digite 'sair' para parar)")
    sender = input("Seu nome: ").strip() or "Anônimo"
    recipient = input("Destinatário: ").strip() or "Todos"
    print(f"Olá {sender}! Envie mensagens para {recipient}:")

    while True:
        try:
            message = input(f"{sender}> ").strip()
            if message.lower() in ['sair', 'exit', 'quit']:
                print("👋 Tchau!")
                break
            if message:
                send_message_to(message, recipient, sender)
        except KeyboardInterrupt:
            print("\n👋 Tchau!")
            break


def print_help():
    print("\nUso:")
    print("  python message_client.py test          # Testa conexão")
    print("  python message_client.py send          # Modo interativo para enviar")
    print("  python message_client.py receive       # Modo interativo para receber")
    print("  python message_client.py help          # Mostra esta ajuda")


def main():
    if len(sys.argv) < 2 or sys.argv[1].lower() == 'help':
        print("🚀 Cliente de Mensagens - Compatível com Servidor Java")
        print("-" * 45)
        print_help()
        return

    command = sys.argv[1].lower()

    print("\n🚀 Cliente de Mensagens")
    print("-" * 45)

    if command == "test":
        test_connection()
    elif command == "send":
        if test_connection():
            interactive_send_mode()
    elif command == "receive":
        if test_connection():
            interactive_receive_mode()
    else:
        print(f"❌ Comando desconhecido: {command}")
        print_help()


if __name__ == "__main__":
    main()