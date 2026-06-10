# Wear OS Build Tool

이 프로젝트는 Docker를 사용하여 로컬 서버에서 Android ADB 명령을 실행할 수 있는 환경을 설정합니다. Flask를 사용하여 ADB 명령을 웹 인터페이스를 통해 실행할 수 있습니다.

## 사용법

1. **files 폴더에 apk을 넣는다**

2. **docker를 설치해 아래 명령어를 실행한다**

```bash
docker-compose build
docker-compose up
```

3. **브라우저에서 [http://localhost:5000](http://localhost:5000) 으로 접속**

## 외부 노출 (선택)

기본적으로 이 도구는 `localhost:5000`에서만 동작합니다. 외부에서 접근해야 할 때는 [ngrok](https://ngrok.com/)을 **호스트에서 별도로** 실행해 5000 포트를 터널링합니다. ngrok을 Docker 이미지에 포함하지 않고 호스트에서 띄우면, 이미지가 가벼워지고 설정도 단순해집니다.

1. **ngrok 설치 및 인증 토큰 등록** (최초 1회):
    - [ngrok](https://ngrok.com/)에서 계정을 만들고 대시보드에서 인증 토큰을 확인합니다.
    - 호스트에 ngrok을 설치한 뒤 토큰을 등록합니다.

    ```bash
    ngrok config add-authtoken your_ngrok_auth_token_here
    ```

2. **컨테이너를 실행한 상태에서** 호스트에서 ngrok으로 5000 포트를 터널링합니다.

    ```bash
    ngrok http 5000
    ```

3. ngrok이 터미널에 표시하는 `https://xxxx.ngrok-free.app` 형태의 URL로 접속합니다.
