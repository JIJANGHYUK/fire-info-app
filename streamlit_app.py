import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# --- 페이지 설정은 항상 맨 위에서 ---
st.set_page_config(page_title="거래처 조회 | 세이프텍", page_icon="🚒")

# --- 구글 스프레드시트 인증 ---
SERVICE_ACCOUNT_FILE = "lateral-raceway-462707-h1-a906d198378b.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID = "1Pjykrj3FtHMQ9aRZnhLAENppBWUZn70__A_p57RG8sc"
SHEET_NAME = "관리현황표"

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

client = gspread.authorize(credentials)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# --- 시트에서 데이터 가져오기 ---
data = sheet.get_all_records(expected_headers=[
    "번호", "대상처", "주소", "관계인/실무자", "수신기위치",
    "펌프실위치", "사용승인일", "종합점검시기", "작동점검시기",
    "연면적", "점검표 전달방법", "출입 비밀번호", "점검(관리)시기"
])

# --- Streamlit UI ---
st.title(":clipboard: 거래처 정보 조회")

names = [row["대상처"] for row in data]
selected_name = st.selectbox("조회할 대상처를 선택하세요:", names)

match = next((row for row in data if row["대상처"] == selected_name), None)

if match:
    st.markdown(f"""
        <div style="border:1px solid #f44336; background-color:#fff8f8; border-radius:10px; padding:20px; line-height:1.9">
            <b>🛑 주소:</b> {match['주소']}<br>
            <b>🔨 관계인/실무자:</b> {match['관계인/실무자']}<br>
            <b>🤝 수신기 위치:</b> {match['수신기위치']}<br>
            <b>🎧 펌프실 위치:</b> {match['펌프실위치']}<br>
            <b>📅 사용승인일:</b> {match['사용승인일']}<br>
            <b>🕰️ 종합점검시기:</b> {match['종합점검시기']}<br>
            <b>🕓 작동점검시기:</b> {match['작동점검시기']}<br>
            <b>🔢 연면적:</b> {match['연면적']} ㎡<br>
            <b>📄 점검표 전달방법:</b> {match['점검표 전달방법']}<br>
            <b>🔐 출입 비밀번호:</b> {match['출입 비밀번호']}<br>
            <b>📓 점검(관리)시기:</b> {match['점검(관리)시기']}
        </div>
    """, unsafe_allow_html=True)
else:
    st.error("정보를 찾을 수 없습니다.")
