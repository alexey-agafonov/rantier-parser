FROM python:3.8-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1
ENV PYTHONPATH /app


COPY ["requirements.txt", "gunicorn.conf", "./"]
RUN pip install -r requirements.txt

COPY rantier-parser/ /app/rantier-parser

ENTRYPOINT ["gunicorn"]
CMD ["-c", "gunicorn.conf", "rantier-parser.app:init_app"]