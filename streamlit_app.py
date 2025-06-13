import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# 🔐 구글 서비스 계정 키 파일 경로
SERVICE_ACCOUNT_FILE = "lateral-raceway-462707-h1-a906d198378b.json"

# 📋 스프레드시트 정보
SPREADSHEET_ID = "1Pjykrj3FtHMQ9aRZnhLAENppBWUZn70__A_p57RG8sc"
SHEET_NAME = "관리현황표"

# 🔐 구글 인증
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# 📄 데이터프리임으로 보기
data = sheet.get_all_records()
df = pd.DataFrame(data)

# 💽️ Streamlit 웹앱 설정
st.set_page_config(page_title="거래체 조회 | 세이프텍", page_icon="🔥")
st.title("📋 거래체 정보 조회")

# 🎯 거래체 선택
target_list = df["대상처"].dropna().unique().tolist()
selected_name = st.selectbox("조회할 대상체를 선택하세요:", target_list)

# 📌 선택된 거래체 정보 표시
info = df[df["대상처"] == selected_name]

if not info.empty:
    row = info.iloc[0]
    st.markdown(f"""
    <div style="border: 1px solid #f55; background-color: #fff5f5; padding: 1rem; border-radius: 10px; font-size: 16px;">
    <b>🔺 주소:</b> {row['주소']}<br>
    <b>🔧 관계인/실무자:</b> {row['관계인/실무자']}<br>
    <b>🔍 수신기 위치:</b> {row['수신기위치']}<br>
    <b>🧰 펑포실 위치:</b> {row['펌프실위치']}<br>
    <b>📅 사용승인일:</b> {row['사용승인일']}<br>
    <b>📊 종합점검시기:</b> {row['종합점검시기']}<br>
    <b>🚰🔧 작동점검시기:</b> {row['작동점검시기']}<br>
    <b>📀 연면적:</b> {row['연면적']} ㎡<br>
    <b>📤 점검표 전달방법:</b> {row['점검표 전달방법']}<br>
    <b>🔐 출입 비밀번호:</b> {row['출입 비밀번호']}<br>
    <b>📅 점검(관리)시기:</b> {row['점검(관리)시기']}<br>
    </div>
    """, unsafe_allow_html=True)
else:
    st.error("정보를 찾을 수 없습니다.")
