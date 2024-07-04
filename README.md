# Wear OS Build Tool

이 프로젝트는 Docker와 ngrok을 사용하여 로컬 서버에서 Android ADB 명령을 실행할 수 있는 환경을 설정합니다. Flask를 사용하여 ADB 명령을 웹 인터페이스를 통해 실행할 수 있습니다.

## 사용법

1. **ngrok 계정 생성 및 인증 토큰 얻기**:
    - [ngrok](https://ngrok.com/) 웹사이트에 접속하여 계정을 만들고 로그인합니다.
    - 대시보드에서 인증 토큰을 확인합니다.

2. **.env 파일 생성**:
    - 프로젝트 루트 디렉토리에 `.env` 파일을 생성합니다.
    - `.env` 파일에 ngrok 인증 토큰을 추가합니다.

    ```env
    NGROK_AUTH_TOKEN=your_ngrok_auth_token_here
    ```

3. **files 폴더에 apk을 넣는다**

4. **docker를 설치해 아래 명령어를 실행한다**

```bash
docker-compose build
docker-compose up
```

5. **컨테이너 로그에서 ngrok가 생성한 임시 url로 접속**
