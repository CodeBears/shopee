# Container/Image name
FROM python:3.10
LABEL maintainer="Johnny Chen<qszwax0935@gmail.com>"

# Prepare packages
ARG WORK_DIR="src"
ENV ENV="/root/.bashrc"
RUN mkdir -p /${WORK_DIR}
WORKDIR /${WORK_DIR}
COPY requirements.txt .
COPY src .

# Install requirement
RUN apt-get -y update && apt-get -y upgrade
RUN touch /var/log/cron.log
RUN apt-get install -y cron
COPY crontab /etc/cron.d/cjob
RUN chmod 0644 /etc/cron.d/cjob

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip --no-cache-dir install -r requirements.txt

