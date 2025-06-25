# Dockerfile
# Developer: G A RAZA
# Docker configuration for AI-Powered Telegram Bot

FROM python:3.10-slim

# Install LaTeX dependencies
RUN apt-get update && apt-get install -y \
    texlive-full \
    texlive-fonts-extra \
    latexmk \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Command to run the bot
CMD ["python", "main.py"]
