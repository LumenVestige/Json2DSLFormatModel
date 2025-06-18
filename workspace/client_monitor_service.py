import asyncio
import time

import websockets
import threading
from collections import deque
from models.index import ws_token, model_monitor_host

# 设置服务器相关信息
host = "0.0.0.0"  # WebSocket 服务器主机
ws_port = 8091  # WebSocket 服务器端口
MAX_CONNECTIONS = 100  # 活跃连接的最大数量
active_connections = deque()  # 活跃连接的队列


async def broadcast_message(message, timeout=5):
    to_remove = []
    for conn in active_connections:
        try:
            # 为每个 conn.send(message) 添加超时
            await asyncio.wait_for(conn.send(message), timeout=timeout)
        except asyncio.TimeoutError:
            print(f"发送消息到 {conn.remote_address} 超时")
            to_remove.append(conn)
        except websockets.ConnectionClosed:
            print(f"连接到 {conn.remote_address} 已关闭")
            to_remove.append(conn)
        except Exception as e:
            print(f"向 {conn.remote_address} 发送消息时发生未知错误: {e}")
            to_remove.append(conn)
    # 移除已关闭或超时的连接
    for conn in to_remove:
        if conn in active_connections:
            active_connections.remove(conn)


# WebSocket 客户端监听函数：连接到 WebSocket 服务器并监听消息
async def client_listen():
    url = f"{model_monitor_host}?token={ws_token}"
    print(f'Connecting to server at {url}')

    while True:
        try:
            async with websockets.connect(url) as websocket:
                print("Connected to the server")

                while True:
                    try:
                        # 设置2分钟超时接收消息
                        message = await asyncio.wait_for(websocket.recv(), timeout=120)
                        print(f"Received: {message}")
                        # 接收到消息后广播出去
                        await broadcast_message(message)
                    except asyncio.TimeoutError:
                        await websocket.close()
                        await asyncio.sleep(5)
                        print("No message received in 2 minutes, reconnecting...")
                        break  # 超时重新连接
        except websockets.ConnectionClosed as e:
            print("Connection closed, retrying...", e)
            await asyncio.sleep(5)  # 重试前等待几秒


# 将监听任务封装为子线程
def start_client_listening():
    while True:
        try:
            loop = asyncio.new_event_loop()  # 创建新的事件循环
            asyncio.set_event_loop(loop)  # 设置事件循环
            loop.run_until_complete(client_listen())  # 运行客户端监听任务
        except Exception as e:
            print('start_client_listening crashed,retry in 5s', e)
            time.sleep(5)


# WebSocket 服务器处理函数：用于处理客户端连接并广播消息
async def server_handler(websocket):
    print(f"New connection from {websocket.remote_address}")  # 调试信息：显示连接的客户端
    if len(active_connections) >= MAX_CONNECTIONS:
        oldest_connection = active_connections.popleft()  # 获取并移除最早的连接
        await oldest_connection.close(code=1001, reason="Connection limit exceeded")

    active_connections.append(websocket)  # 添加新的连接到活跃连接队列
    try:
        await websocket.wait_closed()  # 等待连接关闭
    finally:
        active_connections.remove(websocket)  # 连接关闭时从活跃连接队列中移除
        print(f"Connection closed from {websocket.remote_address}")  # 调试信息：显示断开连接的客户端


# 启动 WebSocket 服务器和客户端监听
async def start_monitor_server():
    # 启动客户端监听
    thread = threading.Thread(target=start_client_listening)
    thread.start()

    # 启动 WebSocket 服务器，广播消息到所有客户端
    start_server = await websockets.serve(server_handler, host, ws_port)
    print(f"WebSocket Serving on ws://{host}:{ws_port}")

    await start_server.wait_closed()  # 等待服务器关闭


if __name__ == "__main__":
    asyncio.run(start_monitor_server())
