import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import pandas as pd

# Google Sheets 인증
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SERVICE_ACCOUNT_JSON = st.secrets["SERVICE_ACCOUNT_JSON"]
info_dict = json.loads(SERVICE_ACCOUNT_JSON)

# 인증 객체 생성
credentials = Credentials.from_service_account_info(
    info_dict,
    scopes=SCOPES
)

# 구글 시트 열기
client = gspread.authorize(credentials)
SPREADSHEET_ID = "1Pjykrj3FtHMQ9aRZnhLAENppBWUZn70__A_p57RG8sc"
SHEET_NAME = "관리현황표"
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# 데이터 가져오기
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Streamlit UI 설정
st.set_page_config(
    page_title="거래처 조회 | (주)콤파스이앤씨",
    page_icon="📋",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        font-family: "NanumGothic", sans-serif;
    }
    .result-box {
        border: 2px solid #e06666;
        border-radius: 10px;
        padding: 1.2em;
        background-color: #fff0f0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📋 '거래처' 정보")

selected_target = st.selectbox("조회할 대상처를 선택하세요:", df["대상처"].unique())

# 조회 결과 표시
target_info = df[df["대상처"] == selected_target]

if not target_info.empty:
    row = target_info.iloc[0]
    info_text = f"""
    <div class="result-box">
    🔺 **주소:** {row['주소']} 🛠️ **관계인/실무자:** {row['관계인/실무자']} / 동일 🔍<br>
    📍 **수신기 위치:** {row['수신기위치']} 🔧 **펌프실 위치:** {row['펌프실위치']} 🗓️ **사용승인일:** {row['사용승인일']}<br>
    📊 **종합점검시기:** {row['종합점검시기']} ⏰ **작동점검시기:** {row['작동점검시기']} 📏 **연면적:** {row['연면적']} ㎡<br>
    📨 **점검표 전달방법:** {row['점검표 전달방법']} 🔐 **출입 비밀번호:** {row['출입 비밀번호']} 🗓️ **점검(관리)시기:** {row['점검(관리)시기']}
    </div>
    """
    st.markdown(f"### 📄 '{selected_target}' 정보")
    st.markdown(info_text, unsafe_allow_html=True)
else:
    st.error("정보를 찾을 수 없습니다.")
