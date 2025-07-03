import json
import asyncio
import websockets

# Nome do usuário atual e o destinatário da conversa
me = ""
dest = ""


# Função responsável por ler a entrada do usuário e enviar a mensagem para o servidor
async def send(ws):
    while True:
        # Usa asyncio.to_thread para não bloquear o event loop com input síncrono
        msg = await asyncio.to_thread(input, "Você: ")
        # Monta o payload da mensagem no formato esperado pelo servidor
        payload = {
            "type": "message",
            "from": me,
            "to": dest,
            "content": msg,
            "encrypted": False,  # Aqui pode futuramente ser alterado para suporte a criptografia
        }
        print("Enviando:", payload)
        # Envia a mensagem como JSON via WebSocket
        await ws.send(json.dumps(payload))


# Função responsável por receber mensagens enviadas para este cliente
async def receive(ws):
    try:
        async for msg in ws:
            print("Recebido bruto:", msg)
            data = json.loads(msg)
            # Exibe a mensagem recebida no formato "remetente: conteúdo"
            print(f"{data['from']}: {data['content']}")
    except websockets.ConnectionClosed:
        # Caso a conexão caia, mostra aviso
        print("Conexão fechada pelo servidor.")


# Função principal que gerencia a conexão e as tarefas assíncronas
async def main():
    global me, dest
    # Solicita o nome do usuário e o destinatário da conversa
    me = input("Digite seu nome de usuário (from): ").strip()
    dest = input("Para quem você quer enviar mensagens (to): ").strip()

    # Endereço do servidor WebSocket
    uri = "ws://127.0.0.1:19001/"

    while True:
        try:
            # Tenta conectar ao servidor
            async with websockets.connect(uri) as ws:
                # Envia mensagem de autenticação inicial (pode ser usada para login futuramente)
                await ws.send(json.dumps({"type": "auth", "token": "fake-jwt-token"}))

                # Cria tarefas assíncronas para envio e recebimento de mensagens
                send_task = asyncio.create_task(send(ws))
                receive_task = asyncio.create_task(receive(ws))

                # Espera apenas a tarefa de recebimento — se ela falhar, reconecta
                await receive_task

        except (
            websockets.ConnectionClosed,
            OSError,
            websockets.InvalidURI,
            websockets.InvalidHandshake,
            asyncio.TimeoutError,
        ) as e:
            # Se ocorrer algum erro na conexão, exibe e tenta reconectar após 5 segundos
            print(f"Erro de conexão: {e}")
            print("Tentando novamente em 5 segundos...")
            await asyncio.sleep(5)


# Executa o loop principal assíncrono
asyncio.run(main())
