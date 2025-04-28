import streamlit as st
import requests
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm

# --- 한글 폰트 설정 (Streamlit Cloud 환경에 맞게 수정) ---
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
# --------------------------------------------------------

# secrets에서 API 불러오기
API_KEY = st.secrets["API_KEY"]
BASE_URL = st.secrets["BASE_URL"]

st.title("SRT 역별 월별 승차 인원 시각화 앱")
st.write("공공데이터를 활용해 선택한 역의 월별 승차 인원을 그래프로 표시합니다.")

# 사용자 입력: 역 이름
station_name = st.text_input("확인하고 싶은 역 이름을 입력하세요 (예: 수서, 동탄, 부산)", "수서")

# 사용자 선택: 그래프 종류
graph_type = st.selectbox(
    "표시할 그래프 타입을 선택하세요",
    ("Bar 그래프", "Line 그래프")
)

# "조회하기" 버튼
if st.button("조회하기"):
    params = {
        "serviceKey": API_KEY,
        "page": 1,
        "perPage": 100
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        response_data = response.json()

        data_list = response_data.get('data', [])

        # 입력한 역 이름으로 데이터 찾기
        station_info = next((item for item in data_list if item.get('승차역') == station_name), None)

        if station_info:
            # 월별 데이터 추출
            monthly_usage = {key: int(value) for key, value in station_info.items() if '년' in key and '월' in key}
            months, counts = zip(*sorted(monthly_usage.items()))

            # 그래프 그리기
            fig, ax = plt.subplots(figsize=(12, 6))

            if graph_type == "Bar 그래프":
                ax.bar(months, counts, color='salmon')
            else:  # Line 그래프
                ax.plot(months, counts, marker='o')

            ax.set_title(f"{station_name} 월별 승차 인원 추이 ({graph_type})")
            ax.set_xlabel("연월")
            ax.set_ylabel("승차 인원 수")
            plt.xticks(rotation=45)

            st.pyplot(fig)
        else:
            st.warning(f"'{station_name}'에 해당하는 역 데이터를 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")

#streamlit run SRT_stream.py
#python -m streamlit run SRT_stream.py

