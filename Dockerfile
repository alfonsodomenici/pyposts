FROM python:3.9-slim-bullseye

ENV FLASK_APP pyposts.py
ENV FLASK_CONFIG production

RUN adduser --disabled-password --disabled-login --shell=/bin/bash --gecos '' pyposts
USER pyposts

WORKDIR /home/pyposts

COPY requirements.txt ./
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations

COPY pyposts.py boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["/bin/bash", "./boot.sh"]