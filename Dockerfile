FROM python:3.11-slim
LABEL authors="Erick Lee"
LABEL version="v1.0"
LABEL python_version="3.11"
LABEL django_version="5.1"

# Set working directory 设置工作目录
WORKDIR /app
# Copy files to workdir 复制文件到工作目录
COPY . /app
# Copy dependencies file 复制依赖文件
COPY requirements.txt requirements.txt

# Install dependencies 安装依赖
RUN python -m pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 挂载所有文件
VOLUME ["/app"]

# 暴露端口
EXPOSE 8000

# 启动服务
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]