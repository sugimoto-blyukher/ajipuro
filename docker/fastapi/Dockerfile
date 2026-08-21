FROM python:3.14-slim-bookworm

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo

WORKDIR /app

# requirements.txtをコピー＆インストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
COPY app ./app
COPY templates ./templates
COPY public ./public

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
