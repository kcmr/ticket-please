FROM python:3.12-slim-bookworm
RUN pip install --no-cache-dir ticketplease
CMD ["tk", "--help"]
