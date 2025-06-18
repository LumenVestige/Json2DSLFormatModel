import asyncio
import json
import socket
import time

import websockets
import psutil
import GPUtil
from collections import deque
from urllib.parse import urlparse, parse_qs

from websockets import InvalidHandshake

from models.index import ws_token

# 设置 WebSocket 服务器的连接数限制和预定义的 token
MAX_CONNECTIONS = 100
REQUIRED_TOKEN = ws_token
active_connections = deque()

# 初始化上一次使用率
previous_cpu_usage = 0
previous_gpu_usage = 0


# 广播函数，向所有活跃连接发送消息
async def broadcast(message, timeout=5):
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


# 获取当前 CPU 和 GPU 使用率
def get_usage():
    cpu_usage = psutil.cpu_percent()
    gpus = GPUtil.getGPUs()
    gpu_usage = gpus[0].load * 100 if gpus else 0
    return cpu_usage, gpu_usage


def get_cpu_usage():
    return psutil.cpu_percent()


# 监控任务：定期检查使用率变化并广播
async def monitor_usage():
    global previous_cpu_usage, previous_gpu_usage
    time1 = time.time()
    while True:
        cpu_usage, gpu_usage = get_usage()
        cpu_usage = round(cpu_usage, 2)
        gpu_usage = round(gpu_usage, 2)
        # message = f"CPU Usage: {cpu_usage}%, GPU Usage: {gpu_usage}%"
        # print(message)
        if cpu_usage != previous_cpu_usage or gpu_usage != previous_gpu_usage:
            message = f"CPU Usage: {cpu_usage}%, GPU Usage: {gpu_usage}%"
            if time.time() - time1 >= 60 * 10:
                time1 = time.time()
                print(message)
            dc = {"cpu": cpu_usage, "gpu": gpu_usage}
            message_json = json.dumps(dc, ensure_ascii=False)
            await broadcast(message_json)
            # await broadcast(message)
            previous_cpu_usage = cpu_usage
            previous_gpu_usage = gpu_usage
        await asyncio.sleep(1)


# 处理 WebSocket 连接，进行 token 校验
async def handler(websocket, path):
    print(f"New connection from {websocket.remote_address} path: {path}")
    # 解析 token
    query = urlparse(path).query
    params = parse_qs(query)
    token = params.get("token", [None])[0]

    # 校验 token
    if token != REQUIRED_TOKEN:
        await websocket.close(code=1008, reason="Invalid or missing token")
        return

    # 连接数限制
    if len(active_connections) >= MAX_CONNECTIONS:
        oldest_connection = active_connections.popleft()
        await oldest_connection.close(code=1001, reason="Connection limit exceeded")

    active_connections.append(websocket)
    try:
        await websocket.wait_closed()
    finally:
        active_connections.remove(websocket)


# 启动服务器和监控任务
async def main():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    async def custom_check(path, request_headers):

        # 解析 token
        query = urlparse(path).query
        params = parse_qs(query)
        token = params.get("token", [None])[0]

        # 校验 token
        if token != REQUIRED_TOKEN:
            return (
                404, [("Content-Type", "text/plain")], '')
        if request_headers.get("Upgrade", "").lower() != "websocket":
            return (
                404, [("Content-Type", "text/plain")], '')

    # 创建 WebSocket 服务器
    server = await websockets.serve(handler, local_ip, 9792, process_request=custom_check)
    print(f"WebSocket Server started on ws://{local_ip}:9792")

    # 开启监控任务
    monitor_task = asyncio.create_task(monitor_usage())

    await server.wait_closed()  # 等待服务器关闭
    await monitor_task  # 等待监控任务结束


if __name__ == "__main__":
    # 运行主程序
    asyncio.run(main())
