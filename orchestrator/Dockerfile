# SPDX-FileCopyrightText: 2025 Taras Paruta (partarstu@gmail.com)
#
# SPDX-License-Identifier: Apache-2.0
FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive

# Create man directories to prevent potential dependency issues with ca-certificates
RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2 && \
    apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jre-headless wget unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the Allure version as an argument
ARG ALLURE_VERSION=2.34.1

# Define environment variables for Allure
ENV ALLURE_HOME=/opt/allure-${ALLURE_VERSION}
ENV PATH="${ALLURE_HOME}/bin:${PATH}"

# Download, extract, and set up Allure Commandline
RUN wget -q https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.zip -O /tmp/allure.zip && \
    unzip /tmp/allure.zip -d /opt && \
    rm /tmp/allure.zip

# Verify Allure installation
RUN allure --version
RUN mkdir "allure-report"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "orchestrator.main:orchestrator_app"]