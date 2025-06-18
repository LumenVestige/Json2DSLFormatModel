import asyncio
import json
import time

import websockets
import threading
from collections import deque
from models.index import ws_token, model_monitor_host
from model_monitor_service import get_usage, get_cpu_usage

# 设置服务器相关信息
host = "0.0.0.0"  # WebSocket 服务器主机
ws_port = 8092  # WebSocket 服务器端口
MAX_CONNECTIONS = 100  # 活跃连接的最大数量
active_connections = deque()  # 活跃连接的队列
# 初始化上一次使用率
previous_cpu_usage = 0
previous_gpu_usage = 0


# 广播函数：将消息发送给所有已连接的客户端
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


async def monitor_usage():
    global previous_cpu_usage, previous_gpu_usage
    while True:
        cpu_usage = get_cpu_usage()
        cpu_usage = round(cpu_usage, 2)
        message = f"CPU Usage: {cpu_usage}%"
        print(message)
        dc = {"cpu": cpu_usage}
        message_json = json.dumps(dc, ensure_ascii=False)
        await broadcast_message(message_json)
        await asyncio.sleep(1)


# 启动 WebSocket 服务器和客户端监听
async def start_monitor_server():
    # 启动 WebSocket 服务器，广播消息到所有客户端
    start_server = await websockets.serve(server_handler, host, ws_port)
    print(f"WebSocket Serving on ws://{host}:{ws_port}")
    # 开启监控任务
    monitor_task = asyncio.create_task(monitor_usage())
    await start_server.wait_closed()  # 等待服务器关闭
    await monitor_task  # 等待监控任务结束


if __name__ == "__main__":
    asyncio.run(start_monitor_server())
