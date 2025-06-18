import asyncio
import websockets

from models.index import ws_token

# 定义服务器地址和端口
host = "localhost"
port = 8091

# 定义正确的 token
token = ws_token


async def listen():
    # 使用 token 构造 WebSocket URL
    # url = f"ws://{host}:{port}?token={token}"
    url = f"ws://{host}:{port}"
    print('url', url)
    # 尝试连接到 WebSocket 服务器
    async with websockets.connect(url) as websocket:
        print("Connected to the server")

        # 持续监听服务器消息
        try:
            while True:
                # 等待接收服务器发送的消息
                message = await websocket.recv()
                print(f"Received: {message}")
        except websockets.ConnectionClosed as e:
            print("Connection closed by the server", e)


# 运行客户端监听任务
asyncio.run(listen())
