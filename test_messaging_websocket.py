import websocket
import threading
import time
import json

WS_URL = "ws://localhost:8080/ws/messages"

SENDER = "TesterWebSocketA"
RECIPIENT = "TesterWebSocketB"
MESSAGE = "Mensagem via WebSocket automatizada"

received_message = None


def receiver_thread():
    """Conecta como RECIPIENT e escuta mensagens"""
    def on_message(ws, message):
        global received_message
        data = json.loads(message)
        if data.get("sender") == SENDER and data.get("message") == MESSAGE:
            received_message = data
            print("✅ Mensagem recebida corretamente!")
            ws.keep_running = False

    def on_error(ws, error):
        print(f"❌ Erro WebSocket no receptor: {error}")

    def on_close(ws, code, msg):
        print("🔌 Conexão do receptor encerrada.")

    ws = websocket.WebSocketApp(
        f"{WS_URL}?user={RECIPIENT}",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever()


def sender_thread():
    """Conecta como SENDER e envia mensagem"""
    def on_open(ws):
        print("📤 Conexão do remetente aberta. Enviando mensagem...")
        payload = {
            "sender": SENDER,
            "recipient": RECIPIENT,
            "message": MESSAGE
        }
        ws.send(json.dumps(payload))
        time.sleep(0.5)
        ws.keep_running = False

    def on_error(ws, error):
        print(f"❌ Erro WebSocket no remetente: {error}")

    def on_close(ws, code, msg):
        print("🔌 Conexão do remetente encerrada.")

    ws = websocket.WebSocketApp(
        f"{WS_URL}?user={SENDER}",
        on_open=on_open,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever()


def test_websocket_messaging():
    global received_message

    print("🚀 Iniciando teste de WebSocket...")

    receiver = threading.Thread(target=receiver_thread)
    receiver.start()

    time.sleep(1)

    sender = threading.Thread(target=sender_thread)
    sender.start()

    timeout = 10
    while timeout > 0 and received_message is None:
        time.sleep(1)
        timeout -= 1

    assert received_message is not None, "❌ Mensagem não recebida via WebSocket!"
    assert received_message.get("sender") == SENDER
    assert received_message.get("recipient") == RECIPIENT
    assert received_message.get("message") == MESSAGE

    print("✅ Teste WebSocket concluído com sucesso.")


if __name__ == "__main__":
    test_websocket_messaging()
