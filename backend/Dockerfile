FROM python:3.12-slim

# 安装 LibreOffice 和字体依赖
RUN apt-get update && \
    apt-get install -y libreoffice fontconfig && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录为 /app
WORKDIR /app

# 拷贝项目文件（包括字体）
COPY . /app

# 安装字体（SimSun 和 Times New Roman）
RUN mkdir -p /usr/share/fonts/truetype/custom && \
    cp /app/SimSun.ttf /usr/share/fonts/truetype/custom/ && \
    cp /app/times.ttf /usr/share/fonts/truetype/custom/ && \
    fc-cache -fv

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建 output 文件夹（用于挂载映射）
RUN mkdir -p /app/output

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

