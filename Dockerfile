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
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip --no-cache-dir install -r requirements.txt
