# 실시간 전력 모니터링 애플리케이션

이 애플리케이션은 스트림릿(Streamlit)을 사용하여 실시간으로 전력 데이터를 모니터링하고 시각화하는 데 사용됩니다. Firebase를 사용하여 데이터를 저장하고 불러옵니다. Firebase Admin SDK를 사용하기 위해 인증 정보가 필요하며, Firebase Realtime Database에는 데이터베이스가 설정되어 있어야 합니다.

## 설치 및 실행

1. **저장소 클론**: 아래 명령을 사용하여 저장소를 클론합니다.
    ```bash
    git clone https://github.com/your_username/your_repository.git
    ```

2. **라이브러리 설치**: 아래 명령을 사용하여 필요한 라이브러리를 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```

3. **Firebase 설정**: Firebase 콘솔에서 Firebase Admin SDK에 필요한 인증 정보를 다운로드하여 `C:/test/test-486a8-firebase-adminsdk-6jl9k-2bf67a04df.json` 경로에 저장합니다. 또한, Firebase Realtime Database에는 데이터베이스가 설정되어 있어야 하며, 데이터베이스 URL은 `https://test-486a8-default-rtdb.firebaseio.com/`로 설정되어 있어야 합니다.

4. **애플리케이션 실행**: 아래 명령을 사용하여 애플리케이션을 실행합니다.
    ```bash
    streamlit run app.py
    ```

## 기능

### 데이터 업데이트 간격 설정

- 사용자는 데이터 업데이트 간격을 1초에서 60초 사이에서 선택할 수 있습니다.

### 실시간 전력값 표시

- 애플리케이션은 실시간으로 현재 전력값을 표시합니다.

### 그래프

- 실시간 전력 데이터를 그래프로 시각화하여 전력의 변화를 추적할 수 있습니다.

### 날짜 및 시간 선택

- 사용자는 원하는 날짜와 시간을 선택하여 해당 시간에 기록된 전력 데이터를 확인할 수 있습니다.

### 통계 정보

- 오늘의 통계 정보를 표시하여 평균 전력, 최소 전력, 최대 전력 및 표준 편차를 확인할 수 있습니다.

### 누적 전력량

- 오늘까지의 누적 전력량을 표시합니다.

### 전력 사용 시간

- 24시간 중 전력 사용이 가장 많은 시간대를 파이 차트로 표시합니다.

## 개발 환경

- Python 3.7 이상
- Streamlit
- Firebase Admin SDK

## 기여

기여는 언제나 환영합니다! 버그를 신고하거나 새로운 기능을 제안해 주세요.

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
