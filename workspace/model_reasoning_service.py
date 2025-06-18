import json
import os
import random
import socket
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import torch

from models.index import create_reasoning_eval_model, get_server_config
from utils.text_utils import text_is_empty

model = create_reasoning_eval_model()
server_config = get_server_config()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # 获取请求的路径
        path = self.path
        print('path', path)
        if path == server_config['dslPath']:
            # 获取请求内容的长度
            content_length = int(self.headers.get('Content-Length', 0))

            # 读取请求体数据
            post_data = self.rfile.read(content_length)

            # 尝试将请求体解析为 JSON 数据
            try:
                data = parse_qs(post_data.decode('utf-8'))
                received_data = data['data'][0] if 'data' in data else None
                token = data['__key'][0] if '__key' in data else None
                print('received_data:', received_data)
                # print('token:', token)
                # 从 data 参数中获取数据
                if text_is_empty(received_data) is False and token == server_config['token']:
                    try:
                        res = model.get_result(received_data)
                        print('parse response:', res)
                        response_data = json.dumps(res['dsl'], ensure_ascii=False)
                        print('response_data:\n', response_data)

                        self.send_response(200)
                    except Exception as e:
                        print('parse error', e)
                        response_data = ''
                        self.send_response(401)
                else:
                    response_data = ''
                    self.send_response(402)
            except Exception as e:
                response_data = ''
                # 返回 400 状态码
                self.send_response(403)

            # 设置响应头
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response_data.encode("utf-8"))
        else:
            # 处理未知路径，返回 404
            self.send_response(404)

            # 设置响应头
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            # 返回 JSON 数据
            self.wfile.write(''.encode("utf-8"))
            return

    def do_GET(self):
        self.send_response(404)

        # 设置响应头
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        # 返回 JSON 数据
        self.wfile.write(''.encode("utf-8"))


# 设置服务器地址和端口
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
port = 9791
server_address = (local_ip, port)

# 创建 HTTP 服务器
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print(f"Serving on http://{local_ip}:{port}")
httpd.serve_forever()
