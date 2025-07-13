import requests
import time

SERVER_URL = "http://localhost:8080/api"

def send_message(sender, recipient, message):
    payload = {
        "sender": sender,
        "recipient": recipient,
        "message": message
    }
    response = requests.post(f"{SERVER_URL}/send-to", json=payload)
    assert response.status_code == 200, f"Erro ao enviar mensagem: {response.text}"
    print("✅ Mensagem enviada com sucesso.")
    return response.json().get("message_id")

def get_messages_for(recipient):
    response = requests.get(f"{SERVER_URL}/receive/{recipient}")
    assert response.status_code == 200, f"Erro ao buscar mensagens: {response.text}"
    return response.json()

def test_messaging_flow():
    sender = "TesterA"
    recipient = "TesterB"
    message = "Mensagem de teste automática"

    print("🔄 Enviando mensagem...")
    message_id = send_message(sender, recipient, message)

    print("🕒 Aguardando processamento da fila (RabbitMQ)...")
    time.sleep(2)

    print("📥 Verificando mensagens recebidas...")
    messages = get_messages_for(recipient)

    found = any(
        msg["sender"] == sender and
        msg["recipient"] == recipient and
        msg["message"] == message
        for msg in messages
    )

    assert found, "❌ Mensagem esperada não foi encontrada!"
    print("✅ Teste passou: mensagem entregue e recebida corretamente.")

if __name__ == "__main__":
    test_messaging_flow()
