FROM alpine:latest


RUN apk add --no-cache python3 py3-urllib3 py3-requests

COPY minecraft-version-change-telegram.py /minecraft-version-change-telegram.py

COPY entrypoint.sh /entrypoint.sh
RUN chmod 555 /entrypoint.sh


CMD ["/entrypoint.sh"]
