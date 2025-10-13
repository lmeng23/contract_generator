# 使用 Ubuntu 最新版本作为基础镜像
FROM ubuntu:latest

# 安装 Python 3.12、LibreOffice 和字体依赖
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.12 python3.12-venv python3.12-dev python3-pip libreoffice fontconfig && \
    rm -rf /var/lib/apt/lists/*

# 设置 Python 和 pip 指向 3.12
RUN ln -sf /usr/bin/python3.12 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# 设置工作目录
WORKDIR /app

# 拷贝项目文件（包括字体）
COPY . /app

# 安装字体（SimSun 和 Times New Roman）
RUN mkdir -p /usr/share/fonts/truetype/custom && \
    cp /app/SimSun.ttf /usr/share/fonts/truetype/custom/ && \
    cp /app/times.ttf /usr/share/fonts/truetype/custom/ && \
    fc-cache -fv

# 安装 Python 依赖
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

# 创建 output 文件夹
RUN mkdir -p /app/output

EXPOSE 8000

# 启动 FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
