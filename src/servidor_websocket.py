import asyncio
import websockets
import json

# Set de conexões ativas
clients = set()


async def handler(ws):
    print("Novo cliente conectado")
    clients.add(ws)
    try:
        async for msg in ws:
            print("Mensagem recebida bruta:", msg)
            try:
                data = json.loads(msg)

                if data["type"] == "auth":
                    print("Token recebido:", data["token"])
                    continue

                elif data["type"] == "message":
                    print(f"Recebido de {data['from']}: {data['content']}")

                    # Reenvia para todos os outros clientes conectados
                    disconnected_clients = set()
                    for client in clients:
                        if client != ws:
                            try:
                                await client.send(msg)
                            except:
                                # Marca como desconectado
                                disconnected_clients.add(client)

                    # Remove os clientes que deram erro
                    clients.difference_update(disconnected_clients)

            except Exception as e:
                print("Erro ao decodificar JSON:", e)

    except websockets.ConnectionClosed:
        print("Cliente desconectado.")

    finally:
        clients.discard(ws)  # Garante remoção


async def main():
    print("Servidor WebSocket rodando em ws://localhost:8000/")
    async with websockets.serve(handler, "localhost", 8000):
        await asyncio.Future()  # mantém o servidor ativo


if __name__ == "__main__":
    asyncio.run(main())
