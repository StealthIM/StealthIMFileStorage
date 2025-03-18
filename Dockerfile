FROM python:3.13.2-alpine

# 设置工作目录
WORKDIR /app

RUN sed -i 's/dl-cdn\.alpinelinux\.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk update && \
    apk add --no-cache make protobuf protobuf-dev

COPY . .

RUN pip install poetry -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

RUN make install_dev

RUN make build

FROM python:3.13.2-alpine

WORKDIR /app

COPY --from=0 /app/dist /app/dist

RUN pip install --no-cache-dir /app/dist/*.whl -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

FROM python:3.13.2-alpine

WORKDIR /app

COPY --from=1 /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

EXPOSE 50052

CMD ["python","-m","stealthimfilestorage","--config=./config/config.toml"]
