import json
import random
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

import requests

from data.index import get_random_jsons
from models.index import create_model_server_request, model_service_local_host, create_model_local_server_request
from utils.common_utils import get_cost_time

random_jsons = get_random_jsons()

def get_res_data():
    random_json = json.dumps(random.sample(random_jsons, 1)[0], ensure_ascii=False)
    print('random_json', random_json)
    # print(json.loads(json.loads(random_json)))
    return json.loads(random_json)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # 获取请求的路径
        path = self.path
        print('path', path)
        if path == '/dsl':
            time1 = time.time()
            # 获取请求内容的长度
            content_length = int(self.headers.get('Content-Length', 0))

            # 读取请求体数据
            post_data = self.rfile.read(content_length)

            # 尝试将请求体解析为 JSON 数据
            try:
                data = parse_qs(post_data.decode('utf-8'))
                received_data = data['data'][0] if 'data' in data else None

                # 从 data 参数中获取数据
                if received_data is not None:
                    try:
                        print('received_data:', json.loads(received_data))
                        request_config = create_model_server_request(received_data)
                        local_request_config = create_model_local_server_request(received_data)
                        print('request_config', request_config['url'], request_config['form'])
                        # try:
                        #     response = requests.post(request_config['url'], data=request_config['form'])
                        #     if response.status_code != 200:
                        #         print('remote server request fail , backup to local:', local_request_config['url'])
                        #         response = requests.post(local_request_config['url'], data=local_request_config['form'])
                        # except Exception as e:
                        #     print('remote server request fail , backup to local:', local_request_config['url'], e)
                        #     response = requests.post(local_request_config['url'], data=local_request_config['form'])
                        i = 0
                        while True:
                            i += 1
                            try:
                                response = requests.post(request_config['url'], data=request_config['form'])
                                if response.status_code != 200:
                                    print('remote server request fail , backup to local:', local_request_config['url'])
                                    response = requests.post(local_request_config['url'],
                                                             data=local_request_config['form'])
                                break
                            except Exception as e:
                                print('remote server request fail', e, 'backup to local:', local_request_config['url'])
                                response = requests.post(local_request_config['url'],
                                                         data=local_request_config['form'])

                        print('response', response.status_code, response.text)
                        if response.status_code == 200:
                            self.send_response(200)
                            response_data = json.dumps(json.loads(response.text), ensure_ascii=False, indent=2)
                        else:
                            response_data = 'parse error'
                            self.send_response(500)

                    except Exception as e:
                        print('parse error', e)
                        response_data = 'parse error'
                        self.send_response(400)
                else:
                    response_data = "'data' field is missing"
                    self.send_response(400)
            except Exception as e:
                response_data = str(e)
                # 返回 400 状态码
                self.send_response(400)

            # 设置响应头
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response_data.encode("utf-8"))
            print('==================> dsl create time cost:', get_cost_time(time1))
        elif path == '/dsl2':
            time1 = time.time()
            # 获取请求内容的长度
            content_length = int(self.headers.get('Content-Length', 0))

            # 读取请求体数据
            post_data = self.rfile.read(content_length)

            # 尝试将请求体解析为 JSON 数据
            try:
                data = parse_qs(post_data.decode('utf-8'))
                received_data = data['data'][0] if 'data' in data else None

                # 从 data 参数中获取数据
                if received_data is not None:
                    try:
                        print('received_data:', json.loads(received_data))
                        request_config = create_model_server_request(received_data)
                        local_request_config = create_model_local_server_request(received_data)
                        print('request_config', request_config['url'], request_config['form'])
                        i = 0
                        while True:
                            i += 1
                            try:
                                response = requests.post(request_config['url'], data=request_config['form'])
                                if response.status_code != 200:
                                    print('remote server request fail , backup to local:', local_request_config['url'])
                                    response = requests.post(local_request_config['url'],
                                                             data=local_request_config['form'])
                                break
                            except Exception as e:
                                print('remote server request fail', e, 'backup to local:', local_request_config['url'])
                                if i > 12:
                                    response = requests.post(local_request_config['url'],
                                                             data=local_request_config['form'])
                                    break
                                print('==================>request fail:,try again:', i)
                                time.sleep(1.1)

                        print('response', response.status_code, response.text)
                        if response.status_code == 200:
                            self.send_response(200)
                            response_data = json.dumps(json.loads(response.text), ensure_ascii=False)
                        else:
                            response_data = 'parse error'
                            self.send_response(500)

                    except Exception as e:
                        print('parse error', e)
                        response_data = '输入json数据不合法:'+str(e)+'\nget input json,please check:\n\n'+received_data+'\n\n'
                        self.send_response(500)
                else:
                    response_data = "'data' field is missing"
                    self.send_response(500)
            except Exception as e:
                response_data = str(e)
                # 返回 400 状态码
                self.send_response(500)

            # 设置响应头
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response_data.encode("utf-8"))
            print('==================> dsl create time cost:', get_cost_time(time1))
        else:
            # 处理未知路径，返回 404
            self.send_response(404)
            response_data = {
                "error": "Not found",
                "status": "fail"
            }
            # 设置响应头
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            # 返回 JSON 数据
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
            return

    def do_GET(self):
        # 获取请求的路径
        path = self.path

        # 根据不同路径返回不同的响应内容
        if path == "/dsl/test":
            try:
                with open('index.html', 'r', encoding='utf-8') as f:
                    # with open('index-debug.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                # 返回 200 状态码
                self.send_response(200)
                self.send_header("Content-Type", "text/html")  # 设置响应为 HTML 类型
                self.end_headers()
                # 返回 HTML 数据
                self.wfile.write(html_content.encode("utf-8"))
            except FileNotFoundError:
                # 如果文件没有找到，返回 404 错误
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "File not found"}).encode("utf-8"))
            return
        elif path == "/create_random_json":
            try:
                res_data = get_res_data()
                print('res_data', res_data)
                json_obj = json.loads(res_data)
                print('json_obj', json_obj)
                # 返回 200 状态码
                self.send_response(200)
                # 设置响应头
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                # 返回 JSON 数据
                # self.wfile.write('123'.encode("utf-8"))
                self.wfile.write(json.dumps(json_obj, ensure_ascii=False).encode("utf-8"))
            except:
                # 返回 200 状态码
                self.send_response(501)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write('error'.encode("utf-8"))
            return
        elif path == "/favicon.ico":
            try:
                with open("favicon.ico", "rb") as f:
                    self.send_response(200)
                    self.send_header("Content-Type", "image/x-icon")
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
        else:
            # 处理未知路径，返回 404
            self.send_response(404)
            # response_data = {
            #     "error": "Not found",
            #     "status": "fail"
            # }
            # 设置响应头
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            # 返回 JSON 数据
            self.wfile.write(''.encode("utf-8"))
            return

    # 设置服务器地址和端口


host = "0.0.0.0"
http_port = 8888


def start_http_server():
    server_address = (host, http_port)
    # 创建 HTTP 服务器
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"http Serving on http://{host}:{http_port}/dsl/test")
    httpd.serve_forever()


if __name__ == "__main__":
    start_http_server()
