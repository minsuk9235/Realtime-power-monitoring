import streamlit as st
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from firebase_admin import credentials, db, initialize_app, get_app
from datetime import datetime, timedelta
from statistics import stdev

# Firebase 인증 및 초기화
cred = credentials.Certificate("")
try:
    app = get_app()
except ValueError:
    app = initialize_app(cred, {'databaseURL': ''})

ref = db.reference('')

# 사용자가 선택한 업데이트 간격을 가져옴
update_interval = st.sidebar.slider("데이터 업데이트 간격 (초)", min_value=1, max_value=60, value=10, key='interval_slider_1')
st.sidebar.write(f"데이터는 매 {update_interval} 초마다 업데이트됩니다.")

# 페이지 자동 새로 고침 설정
refresh_interval = st_autorefresh(interval=update_interval * 1000, key="datarefresh_real_power")  # milliseconds

st.sidebar.title("페이지 선택")
selected_page = st.sidebar.radio("페이지", ["실시간 전력 모니터링", "통계 정보"])

if selected_page == "실시간 전력 모니터링":  
    
    st.markdown("<h1 style='text-align: center; color: black;'>실시간 전력 모니터링</h1>", unsafe_allow_html=True)

    # 현재 전력값 가져오기
    def fetch_data():
        data = ref.get()
        if data:
            # Firebase에서 데이터 가져오기
            return [(datetime.strptime(key, "%Y-%m-%d %H:%M:%S"), value) for key, value in data.items()]
        else:
            return []

    # 데이터 초기화 및 갱신
    if datetime.now().hour == 0 and datetime.now().minute == 0:
        # 자정에 데이터 초기화
        ref.delete()  # Firebase 데이터 삭제
        st.experimental_rerun()

    # 현재 날짜 가져오기
    current_date = datetime.now().date()

    # 데이터 가져오기
    data = fetch_data()

    # 오늘의 데이터만 필터링
    today_data = [(time, value) for time, value in data if time.date() == current_date]

    # 1. 실시간 전력 모니터링 글자
    if data:
        # 데이터가 있을 경우
        current_power = data[-1][1]
        st.subheader(f"현재 전력값: {current_power} [W]")

    # 2. 그래프
    st.subheader("그래프")

    def get_recent_data(data, num_points):
        # 최근 데이터 가져오기
        if len(data) > num_points:
            return data[-num_points:]
        else:
            return data

    def plot_graph(data):
        # 그래프 그리기
        x = [item[0] for item in data]
        y = [item[1] for item in data]
        min_y = min(y)
        max_y = max(y)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, y, '-o', color='skyblue', linewidth=2, markersize=8, markeredgecolor='black', markeredgewidth=1, label='Real Power')
        
        # 추세선 추가
        z = np.polyfit(range(len(y)), y, 1)
        p = np.poly1d(z)
        ax.plot(x, p(range(len(y))), color='orange', linestyle='--', linewidth=2, label='Trend Line')
        
        # 최신 지점에서 실시간 전력 값 추가
        latest_time, latest_value = data[-1]
        ax.text(latest_time, latest_value, f'{latest_value} [W]', fontsize=10, ha='right', va='bottom', color='black')
        
        ax.set_xlabel('Time')
        ax.set_ylabel('Real Power [W]')
        ax.set_title('Real Power Over Time')
        ax.set_ylim(min_y - 0.1 * abs(min_y), max_y + 0.1 * abs(max_y))
        ax.set_xlim(x[0], x[-1])
        ax.grid(True)
        ax.legend()

        st.pyplot(fig)

    data = fetch_data()
    num_points = st.session_state.get("num_points", min(20, len(data)))  # 이전에 설정된 데이터 양 불러오기

    # 3. 표시할 데이터양 설정
    num_points = st.number_input("그래프에 출력할 데이터 양", min_value=1, value=20, key='num_points')
    st.write(f"총 누적 데이터: {len(data)}")
    recent_data = get_recent_data(data, num_points)

    # 4. 그래프 출력
    plot_graph(recent_data)

    # 5. 날짜 및 시간 선택
    st.subheader("날짜 및 시간 선택")

    # 사용자가 선택한 날짜 입력
    selected_date = st.date_input("날짜", value=datetime.now().date(), key='selected_date')

    # 현재 시간 가져오기
    current_hour = datetime.now().hour

    # 시간은 1시간 단위로 선택, 현재 시간을 기본 값으로 설정
    selected_hour = st.slider("시간", min_value=0, max_value=23, value=current_hour, step=1, key='selected_hour')

    # 선택된 날짜와 시간에 해당하는 데이터 필터링
    selected_data = [(time, value) for time, value in data if time.date() == selected_date and time.hour == selected_hour]

    # 선택된 데이터가 있을 경우에만 체크박스 생성
    if selected_data:
        show_selected_data = st.checkbox("선택된 데이터 표시")
        if show_selected_data:
            st.subheader("선택된 데이터")
            st.write("```")
            st.write(pd.DataFrame(selected_data, columns=['시간', '전력량 [W]']))
            st.write("```")
    else:
        st.write("선택된 시간에 대한 데이터가 없습니다.")


    # 6. 전체 데이터
    st.subheader("전체 데이터")
    PAGE_SIZE = 10
    num_pages = len(data) // PAGE_SIZE + 1
    page_number = st.number_input("페이지 번호", min_value=1, max_value=num_pages, value=1, key='page_number')
    start_index = (page_number - 1) * PAGE_SIZE
    end_index = min(len(data), page_number * PAGE_SIZE)
    with st.expander("전체 데이터 보기"):
        with st.container():
            st.write(f"페이지: {page_number} / {num_pages}, 데이터 범위: {start_index + 1} - {end_index}, 전체 데이터 양: {len(data)}")
            for idx, (timestamp, value) in enumerate(data[start_index:end_index], start=start_index + 1):
                st.write(f"{idx}. 시간: {timestamp}, 전력량: {value} [W]")

# 페이지 자동 새로 고침 설정
    efresh_interval = st_autorefresh(interval=update_interval * 1000, key="datarefresh")  # milliseconds

elif selected_page == "통계 정보":

    st.markdown("<h1 style='text-align: center; color: black;'>통계 정보</h1>", unsafe_allow_html=True)

    # 데이터 가져오기
    def fetch_data():
        data = ref.get()
        if data:
            # Firebase에서 데이터 가져오기
            return [(datetime.strptime(key, "%Y-%m-%d %H:%M:%S"), value) for key, value in data.items()]
        else:
            return []

    # 라디오 버튼으로 기간 선택
    statistics_period = st.radio("통계 기간 선택", options=["오늘", "일주일", "한 달"])

    data = fetch_data()

    if statistics_period == "오늘":
        start_date = datetime.now().date()
        end_date = start_date
        st.subheader(f"오늘 통계 정보 ({start_date} ~ {end_date})")
        period_data = [(time, value) for time, value in data if time.date() == start_date]
    elif statistics_period == "일주일":
        # 일주일 전 데이터 구하기
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=6)
        st.subheader(f"일주일 통계 정보 ({start_date} ~ {end_date})")
        period_data = [(time, value) for time, value in data if start_date <= time.date() <= end_date]
    elif statistics_period == "한 달":
        # 한 달 전 데이터 구하기
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=29)
        st.subheader(f"한 달 통계 정보 ({start_date} ~ {end_date})")
        period_data = [(time, value) for time, value in data if start_date <= time.date() <= end_date]

    if period_data:
        # 통계 정보 계산
        values = [item[1] for item in period_data]
        average_power = sum(values) / len(values)
        min_power = min(values)
        max_power = max(values)
        standard_deviation_power = stdev(values)
        
    # 통계 정보를 하나의 표로 표시
    stats_df = pd.DataFrame({
        "평균": [average_power],
        "최솟값": [min_power],
        "최댓값": [max_power],
        "표준편차": [standard_deviation_power]
    }, index=["전력(W)"])

    # 소수점 둘째 자리까지 반올림
    stats_df = stats_df.round(2)

    # DataFrame 출력
    st.write(stats_df)

    # 선택된 기간의 누적 전력량 계산 (Wh -> kWh)
    cumulative_power_wh = sum(value for _, value in period_data)
    cumulative_power_kwh = cumulative_power_wh / 1000  # Wh to kWh

    # 누적 전력량 출력 (Wh -> kWh)
    st.write(f"누적 전력량: {cumulative_power_kwh:.2f} [kW]")

    # 8. 원형 그래프로 24시간 중 가장 많이 사용한 시간대 표시
    st.subheader("전력 사용 시간")

    if period_data:
        hourly_power = np.zeros(24)  # 시간당 전력 소비량을 저장하기 위한 배열 초기화

        for time, power in period_data:
            hour = time.hour
            hourly_power[hour] += power

        max_power_hour = np.argmax(hourly_power)
        max_power = hourly_power[max_power_hour]

        non_zero_hourly_power = [power for power in hourly_power if power != 0]
        non_zero_labels = [f"{hour} hour ({power/sum(non_zero_hourly_power)*100:.2f} %)" for hour, power in enumerate(hourly_power) if power != 0]

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(non_zero_hourly_power, labels=non_zero_labels, startangle=90, counterclock=False)
        ax.set_title("Power Consumption by Hour in a Day")
        st.pyplot(fig)
        st.write(f"24시간 내에 전력 소비량이 가장 많은 시간: {max_power_hour} 시, 누적 소비전력: {max_power/1000:.2f} [kW]")

        # 시간당 누적 전력 소비량(kW)을 간결한 형식으로 표시
        st.subheader("시간별 누적 전력 소비량(kW)")
        hour_list = [f"{hour} hour" for hour, power in enumerate(hourly_power)]
        power_list = [power / 1000 for power in hourly_power]
        df = pd.DataFrame({"시간": hour_list, "전력 소비량(kW)": power_list})  # 데이터프레임 생성

        # 표 스타일 설정
        st.write(f"날짜: {start_date} ~ {end_date}")  # 선택한 기간 표시
        st.dataframe(df.T.style.set_properties(**{'text-align': 'center', 'font-size': '20px'})\
            .set_table_styles([{'selector': 'th', 'props': [('font-size', '16px'), ('text-align', 'center')]}]))

    # 데이터 초기화 및 갱신
    if datetime.now().hour == 0 and datetime.now().minute == 0:
        ref.delete()  # Firebase 데이터 삭제
        st.experimental_rerun()
