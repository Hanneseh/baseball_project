FROM tiangolo/uwsgi-nginx-flask:python3.6
LABEL maintainer="maintainer"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8050

CMD [ "python", "index.py" ]

ENV NGINX_WORKER_PROCESSES auto