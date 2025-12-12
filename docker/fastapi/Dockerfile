FROM python:3.14-slim-bookworm

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo

# 作業ディレクトリを設定
#WORKDIR /app

# requirements.txtをコピー＆インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#appをコピー
COPY ./app /app

#ポート開放
EXPOSE 8080

# 本番用CMD
CMD ["uvicorn",  "main:app", "--reload"]
