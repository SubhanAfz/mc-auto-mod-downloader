FROM ghcr.io/astral-sh/uv:python3.13-alpine
COPY . .
RUN chmod +x run.sh

ENTRYPOINT [ "./run.sh" ]