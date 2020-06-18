FROM python:3.8-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1
ENV PYTHONPATH /app


COPY ["requirements.txt", "gunicorn.conf", "./"]
RUN pip install -r requirements.txt

COPY rantier_parser /app/rantier_parser

ENTRYPOINT ["gunicorn"]
CMD ["-c", "gunicorn.conf", "rantier_parser.app:init_app"]