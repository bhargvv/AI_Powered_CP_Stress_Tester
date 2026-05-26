
FROM ubuntu:22.04


ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    g++ \
    gcc \
    openjdk-17-jdk \
    build-essential \
    curl && \
    rm -rf /var/lib/apt/lists/*



RUN ln -s /usr/bin/python3 /usr/bin/python



WORKDIR /workspace




ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1



RUN python --version
RUN g++ --version
RUN javac -version



CMD ["bash"]