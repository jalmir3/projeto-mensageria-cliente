from datetime import datetime
import json
import asyncio
import websockets

me = ""
recipient = ""


# Função responsável por ler a entrada do usuário e enviar a mensagem para o servidor
async def send(ws):
    while True:
        # Não é usado input pois o input é sincrono
        msg = await asyncio.to_thread(input, ">")  # entrada simples

        payload = {
            "sender": me,
            "message": msg,
            "recipient": recipient,
        }
        await ws.send(json.dumps(payload))


# Função responsável por receber mensagens enviadas para este cliente
async def receive(ws):
    try:
        async for msg in ws:
            data = json.loads(msg)

            sender = data.get("sender", "Desconhecido")
            content = data.get("message", "")
            timestamp = datetime.now().strftime("%H:%M")

            if sender == me:
                ...
                # print(f"[{timestamp}] Você (para {data.get('recipient')}): {content}")
            else:
                print(f"[{timestamp}] {sender}: {content}")

    except websockets.ConnectionClosed:
        print("⚠️ Conexão fechada pelo servidor.")


# Função principal que gerencia a conexão e as tarefas assíncronas
async def main():
    global me, recipient
    me = input("Seu nome de usuário: ").strip()
    recipient = input("Enviar mensagens para: ").strip()

    uri = f"ws://127.0.0.1:8080/ws/messages?user={me}"

    while True:
        try:
            async with websockets.connect(uri) as ws:
                print(f"🔗 Conectado como '{me}'. Enviando para '{recipient}'\n")

                send_task = asyncio.create_task(send(ws))
                receive_task = asyncio.create_task(receive(ws))

                await receive_task

        except (
            websockets.ConnectionClosed,
            OSError,
            websockets.InvalidURI,
            websockets.InvalidHandshake,
            asyncio.TimeoutError,
        ) as e:
            print(f"❌ Erro de conexão: {e}")
            print("⏳ Tentando reconectar em 5 segundos...\n")
            await asyncio.sleep(5)


# Executa o loop principal assíncrono
asyncio.run(main())
