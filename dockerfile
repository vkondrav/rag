FROM python:3

COPY . /app

WORKDIR /app

RUN chmod +x run.sh

CMD ["./run.sh"]