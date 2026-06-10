FROM ubuntu:20.04

ENV ANDROID_SDK_URL="https://dl.google.com/android/repository/platform-tools-latest-linux.zip"
ENV ANDROID_HOME="/usr/local/android-sdk"
ENV PATH="${ANDROID_HOME}/platform-tools:${PATH}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    unzip \
    wget \
    curl \
    openjdk-8-jdk \
    python3 \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p ${ANDROID_HOME} && \
    wget -q ${ANDROID_SDK_URL} -O /tmp/platform-tools.zip && \
    unzip /tmp/platform-tools.zip -d ${ANDROID_HOME} && \
    rm /tmp/platform-tools.zip

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY . /app
WORKDIR /app

CMD ["python3", "./app.py"]
