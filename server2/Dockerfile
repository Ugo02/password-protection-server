FROM python:3.8-slim

# Install dependencies for building Tink
RUN apt-get update && apt-get install -y curl gnupg default-jdk ca-certificates unzip && rm -rf /var/lib/apt/lists/*

# Install Bazelisk for arm64
RUN curl -L -o /usr/local/bin/bazel https://github.com/bazelbuild/bazelisk/releases/download/v1.13.2/bazelisk-linux-arm64
RUN chmod +x /usr/local/bin/bazel

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and the key files
COPY app.py ./
COPY master_key.json ./
COPY encrypted_keyset.json ./

EXPOSE 5001
CMD ["python", "app.py"]
