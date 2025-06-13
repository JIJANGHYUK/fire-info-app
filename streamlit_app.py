import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials

# --- Streamlit 페이지 설정 ---
st.set_page_config(page_title="거래처 조회 | 세이프텍", page_icon="🚒")

# --- 서비스 계정 인증 ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SERVICE_ACCOUNT_JSON = st.secrets["SERVICE_ACCOUNT_JSON"]
info = json.loads(SERVICE_ACCOUNT_JSON)
credentials = Credentials.from_service_account_info(info, scopes=SCOPES)

# --- Google Sheet 정보 ---
SPREADSHEET_ID = "1Pjykrj3FtHMQ9aRZnhLAENppBWUZn70__A_p57RG8sc"
SHEET_NAME = "관리현황표"

client = gspread.authorize(credentials)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# --- 데이터 가져오기 ---
data = sheet.get_all_records(expected_headers=[
    "번호", "대상처", "주소", "관계인/실무자", "수신기위치", "펌프실위치", "사용승인일",
    "종합점검시기", "작동점검시기", "연면적", "점검표 전달방법", "출입 비밀번호", "점검(관리)시기"
])

# --- 대상처 목록 생성 ---
names = [row["대상처"] for row in data]
selected_name = st.selectbox("조회할 대상처를 선택하세요:", sorted(names))

# --- 선택된 대상 정보 표시 ---
result = next((row for row in data if row["대상처"] == selected_name), None)

if result:
    st.markdown(f"""
    ## 📄 '{result['대상처']}' 정보
    <div style='border:1px solid #f28b82; background-color:#fff5f5; padding:15px; border-radius:10px;'>
    🔺 **주소:** {result['주소']}  
    🔨 **관계인/실무자:** {result['관계인/실무자']}  
    🔎 **수신기 위치:** {result['수신기위치']}  
    🔧 **펌프실 위치:** {result['펌프실위치']}  
    📅 **사용승인일:** {result['사용승인일']}  
    📊 **종합점검시기:** {result['종합점검시기']}  
    ⏰ **작동점검시기:** {result['작동점검시기']}  
    📄 **연면적:** {result['연면적']}  
    🗓 **점검표 전달방법:** {result['점검표 전달방법']}  
    🔐 **출입 비밀번호:** {result['출입 비밀번호']}  
    🗒 **점검(관리)시기:** {result['점검(관리)시기']}  
    </div>
    """, unsafe_allow_html=True)
else:
    st.error("정보를 찾을 수 없습니다.")
