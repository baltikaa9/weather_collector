FROM python:3.11-slim-buster
COPY . .
WORKDIR .

RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install -r requirements.txt
CMD ["python", "main.py", "collect"]