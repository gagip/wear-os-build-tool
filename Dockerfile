FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV ANDROID_SDK_URL="https://dl.google.com/android/repository/platform-tools-latest-linux.zip"
ENV ANDROID_HOME="/usr/local/android-sdk"
ENV PATH="${ANDROID_HOME}/platform-tools:${PATH}"

# uv가 /app 밖에 가상환경을 만들도록 지정 (docker-compose의 .:/app 볼륨이 .venv를 가리지 않게)
ENV UV_PROJECT_ENVIRONMENT="/opt/venv"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    unzip \
    wget \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p ${ANDROID_HOME} && \
    wget -q ${ANDROID_SDK_URL} -O /tmp/platform-tools.zip && \
    unzip /tmp/platform-tools.zip -d ${ANDROID_HOME} && \
    rm /tmp/platform-tools.zip

WORKDIR /app

# 의존성만 먼저 설치해 레이어 캐시를 활용한다 (런타임 전용, dev 그룹 제외)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

ENV PATH="/opt/venv/bin:${PATH}"

COPY . /app

CMD ["python", "app.py"]
