FROM ubuntu:20.04

ENV AZURE_CLIENT_ID=#{Az-Client-Id}#
ENV AZURE_CLIENT_SECRET=#{Az-Client-Secret}#
ENV AZURE_TENANT_ID=#{Az-Tenant-Id}#

COPY main.py /root/main.py

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    curl \
    python3 \
    python3-pip \
    tar \
    vim \
    wget

RUN pip3 install flask azure.identity azure-devops msrest

WORKDIR /root

ENTRYPOINT python3 main.py
