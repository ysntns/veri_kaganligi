FROM mcr.microsoft.com/devcontainers/python:3.11

# Node.js kurulumu
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g yarn

# Sistem bagimliliklari
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-tur \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Calisma dizini
WORKDIR /workspace

# Kullanici ayarlari
USER vscode
