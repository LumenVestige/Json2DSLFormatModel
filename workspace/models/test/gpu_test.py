import torch
import pycuda.driver as cuda

print(torch.cuda.is_available())

cuda.init()
device = cuda.Device(0)  # 获取第一个 GPU
print(f"GPU Name: {device.name()}")
print(f"Memory: {device.total_memory() // (1024 ** 2)} MB")

import GPUtil

# 获取所有 GPU 的信息
gpus = GPUtil.getGPUs()

for gpu in gpus:
    print(f"GPU: {gpu.name}")
    print(f"  GPU Load: {gpu.load * 100}%")
    print(f"  Memory Used: {gpu.memoryUsed}MB / {gpu.memoryTotal}MB")
    print(f"  GPU Memory Free: {gpu.memoryFree}MB")
    print(f"  GPU Utilization: {gpu.memoryUtil * 100}%")
    print(f"  GPU Temperature: {gpu.temperature} °C")

import subprocess


def get_gpu_usage_with_nvidia_smi():
    result = subprocess.run(
        ['nvidia-smi', '--query-gpu=utilization.gpu,temperature.gpu,memory.used,memory.free,memory.total',
         '--format=csv,noheader,nounits'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    print(output)


# 调用该函数显示 GPU 负载
get_gpu_usage_with_nvidia_smi()
