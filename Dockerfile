# 使用 Ubuntu 22.04 作为基础镜像
FROM ubuntu:22.04

# 设置工作目录（可根据需要更改）
WORKDIR /workspace

# 更新包列表
RUN apt-get update

RUN apt-get install -y net-tools

# 安装 Python3 和 pip
RUN apt-get install -y python3 python3-pip

# 安装 wget
RUN apt-get install -y wget

# 安装 Node.js 和 npm
RUN apt-get install -y \
    curl \
    gnupg2 \
    lsb-release \
    ca-certificates \
    sudo \
    build-essential
RUN curl -fsSL https://deb.nodesource.com/setup_23.x | bash - && \
    apt-get install -y nodejs

# 清理不再需要的 apt 缓存
RUN rm -rf /var/lib/apt/lists/*

# 检查安装的版本
RUN python3 --version
RUN pip3 --version
RUN node -v
RUN npm -v

RUN pip3 install requests
RUN pip3 install transformers
## For CUDA 12.1
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
RUN pip3 install beautifulsoup4
RUN pip3 install jsonfixer
RUN pip3 install psutil gputil websockets
RUN npm install pm2 -g

# 将指定的本地目录复制到容器中的工作目录中
COPY workspace/ /workspace/

RUN chmod +x /workspace/start.sh

# 设置容器启动时默认执行的命令
CMD ["sh", "/workspace/start.sh"]