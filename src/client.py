import json
import websockets
import asyncio

me = ""
dest = ""


async def send(ws):
    while True:
        msg = input("Você: ")
        payload = {
            "type": "message",
            "from": me,
            "to": dest,
            "content": msg,
            "encrypted": False,
        }
        print("Enviando:", payload)
        await ws.send(json.dumps(payload))


async def receive(ws):
    try:
        async for msg in ws:
            print("Recebido bruto:", msg)
            data = json.loads(msg)
            print(f"{data['from']}: {data['content']}")
    except websockets.ConnectionClosed:
        print("Conexão fechada pelo servidor.")


async def main():
    global me, dest
    me = input("Digite seu nome de usuário (from): ").strip()
    dest = input("Para quem você quer enviar mensagens (to): ").strip()
    uri = "ws://localhost:8000/"

    while True:
        try:
            async with websockets.connect(uri) as ws:
                await ws.send(json.dumps({"type": "auth", "token": "fake-jwt-token"}))

                send_task = asyncio.create_task(send(ws))
                receive_task = asyncio.create_task(receive(ws))

                # Aguarda apenas o receive. Se der erro, desconecta.
                await receive_task

        except (
            websockets.ConnectionClosed,
            OSError,
            websockets.InvalidURI,
            websockets.InvalidHandshake,
            asyncio.TimeoutError,
        ) as e:
            print(f"Erro de conexão: {e}")
            print("Tentando novamente em 5 segundos...")
            await asyncio.sleep(5)


asyncio.run(main())
