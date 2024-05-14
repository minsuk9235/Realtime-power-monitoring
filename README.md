# 실시간 전력 모니터링 및 통계 정보

이 프로젝트는 Streamlit을 사용하여 실시간으로 전력을 모니터링하고 통계 정보를 제공하는 애플리케이션입니다. Firebase Realtime Database에서 전력 데이터를 가져와 사용자는 웹 앱을 통해 데이터를 시각화하고 통계를 확인할 수 있습니다.

## 사용된 기술

- Python
- Streamlit
- Firebase Realtime Database
- Matplotlib
- Pandas

## 설치 및 실행

1. 저장소를 클론합니다:

```bash
git clone https://github.com/yourusername/your-repo.git
```

2. 필요한 라이브러리를 설치합니다:

```bash
pip install -r requirements.txt
```

3. Firebase 설정

   - Firebase 프로젝트를 생성하고 애플리케이션을 추가합니다.
   - Firebase Realtime Database를 사용하도록 설정하고 해당 URL을 코드에 반영합니다.
   - 서비스 계정 키를 생성하고 해당 JSON 파일을 프로젝트 디렉토리에 추가합니다.
   - 코드에서 JSON 파일의 경로를 수정하여 로컬 디렉토리에 있는 파일을 참조하도록 합니다.

4. 애플리케이션을 실행합니다:

```bash
streamlit run your_app.py
```

## 기능

### 로그인 및 회원가입

![image](https://github.com/minsuk9235/Streamlit-firebase/assets/169111946/019bf76c-e6db-4100-b060-7d7d4326a648)
![image](https://github.com/minsuk9235/Realtime-power-monitoring/assets/169111946/f62e802c-5cef-444f-b687-1baccf2386dd)

- 사용자는 로그인 또는 회원가입을 할 수 있습니다.
- Firebase Authentication을 사용하여 사용자를 인증합니다.
- 회원가입 시 파이어 베이스 경로를 지정하여 자신의 데이터를 모니터링할 수 있습니다.

### 데이터 업데이트 간격 설정

![image](https://github.com/minsuk9235/Streamlit-firebase/assets/169111946/a644495e-1436-499d-b1ec-95bbac343fa3)


- 사용자는 데이터 업데이트 간격을 1초에서 60초 사이에서 선택할 수 있습니다.

### 실시간 전력값 표시

![image](https://github.com/minsuk9235/Streamlit-firebase/assets/169111946/c9883d1e-b857-4090-af9e-77fff4ea47d2)

- 애플리케이션은 실시간으로 현재 전력값을 표시합니다.

### 그래프

![image](https://github.com/minsuk9235/Realtime-power-monitoring/assets/169111946/89e62e48-6b40-47c6-9975-ea3a011c3eea)

- 실시간 전력 데이터를 그래프로 시각화하여 전력의 변화를 추적할 수 있습니다.
- 그래프에 출력할 테이터 양을 결정할 수 있습니다.

### 날짜 및 시간 선택

![image](https://github.com/minsuk9235/Streamlit-firebase/assets/169111946/6e3fcce2-52e6-4e08-8db4-d077dc3c26d5)

- 사용자는 원하는 날짜와 시간을 선택하여 해당 시간에 기록된 전력 데이터를 확인할 수 있습니다.

### 통계 정보

![image](https://github.com/minsuk9235/Streamlit-firebase/assets/169111946/7e54aef0-5732-4fb1-a13e-e01fdcc853e6)

- 오늘의 통계 정보를 표시하여 평균 전력, 최소 전력, 최대 전력 및 표준 편차를 확인할 수 있습니다.

### 누적 전력량

![image](https://github.com/minsuk9235/Streamlit-firebase/assets/169111946/409b2b20-f4cb-4adb-bfc7-bbe46c562006)


- 누적 전력량을 표시합니다.

### 전력 사용 시간

![image](https://github.com/minsuk9235/Streamlit-firebase/assets/169111946/a4286740-35e9-4e53-86dd-004026ea7ca1)

- 24시간 중 전력 사용이 가장 많은 시간대를 파이 차트로 표시합니다.


## 기여

이 프로젝트에 관심이 있거나 버그를 발견한 경우, 이슈를 제출하거나 풀 리퀘스트를 보내주세요!


## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
