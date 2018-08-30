FROM python:3.6.2-slim

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev libffi-dev libav-tools libavcodec-extra sox libsox-fmt-all opus-tools --no-install-recommends

EXPOSE 8000

add . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
