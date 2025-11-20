import streamlit as st
from openai import OpenAI
import os

# ✅ OpenAI 클라이언트 생성 (신버전 대응)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Streamlit UI 설정
st.set_page_config(page_title="토론 참여형 AI", layout="centered")
st.title("🗣️ 토론 참여형 AI")
st.markdown("GPT를 이용한 한국어 토론 시뮬레이터")

# ✅ 프리미엄 버튼 (제한 없이 시각용)
st.sidebar.markdown("## 💎 프리미엄 모드")
if st.sidebar.button("🚀 프리미엄으로 전환"):
    st.session_state["is_premium"] = True
    st.sidebar.success("프리미엄 모드 활성화됨")
elif "is_premium" not in st.session_state:
    st.session_state["is_premium"] = False

if st.session_state["is_premium"]:
    st.markdown("### 🌟 프리미엄 모드 활성화 중")
else:
    st.markdown("💡 현재는 기본 모드입니다.")

# ✅ 사용자 입력: 토론 주제
st.markdown("---")
topic = st.text_input("토론 주제를 입력하세요", placeholder="예: AI는 인간 교사를 대체할 수 있는가")
start = st.button("🟢 토론 시작")

# ✅ GPT 호출 함수 (JSON + 본문 출력 요청)
def call_llm(role, turn, move_type, topic):
    system = (
        f"너는 논리적인 토론 AI야. 주제는 '{topic}' 이고, "
        "모든 응답은 반드시 JSON 형식으로 시작하고, 그 아래 줄부터 사람이 읽을 수 있는 한국어 토론문 본문을 출력해."
    )
    user_content = (
        f'{{"role":"{role}","turn":{turn},"move_type":"{move_type}"}}\n'
        f"주제: {topic}에 대해 {move_type} 역할의 입장에서 응답해줘."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_content}
        ],
        temperature=0.7,
        max_tokens=800
    )
    return response.choices[0].message.content

# ✅ 토론 단계 실행 함수
def run_debate(topic):
    st.markdown("---")
    st.subheader("🔹 1. 개회사 (찬성측)")
    st.write(call_llm("Debater_A", 1, "constructive", topic))

    st.subheader("🔹 2. 반박 (반대측)")
    st.write(call_llm("Debater_B", 2,