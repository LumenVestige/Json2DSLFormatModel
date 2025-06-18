#!/bin/bash

ifconfig

# 启动模型相关服务
echo "start model services"
# 推理服务
pm2 start ./model_reasoning_service.py --name model_reasoning_service --interpreter python3

# 启动客户端相关服务
echo "start client services"
pm2 start ./client_monitor_service.py --name client_monitor_service --interpreter python3

#资源监控服务
# 本地CPU资源监控
pm2 start ./model_local_monitor_service.py --name model_monitor_service --interpreter python3
# 远程GPU服务器监控
#pm2 start ./model_monitor_service.py --name model_monitor_service --interpreter python3

# 启动app服务
python3 ./client_app_service.py