import streamlit as st
from openai import OpenAI
import os

# ✅ 클라이언트 생성
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Streamlit 페이지 설정
st.set_page_config(page_title="토론 참여형 AI", layout="centered")
st.title("🗣️ 토론 참여형 AI")
st.markdown("GPT를 이용한 한국어 토론 시뮬레이터")

# ✅ 프리미엄 모드 버튼
st.sidebar.markdown("## 💎 프리미엄 모드")
is_premium = st.sidebar.button("🚀 프리미엄으로 전환")

# ✅ 세션 상태 저장
if is_premium:
    st.session_state["is_premium"] = True
    st.sidebar.success("✅ 프리미엄 모드가 활성화되었습니다!")
elif "is_premium" not in st.session_state:
    st.session_state["is_premium"] = False

# ✅ 현재 모드 표시
if st.session_state["is_premium"]:
    st.markdown("### 🌟 프리미엄 모드 활성화 중")
else:
    st.markdown("💡 현재는 기본 모드입니다.")

# ✅ 주제 입력 받기
topic = st.text_input("토론 주제를 입력하세요", placeholder="예: AI는 인간 교사를 대체할 수 있는가")
start_button = st.button("🟢 토론 시작")

# ✅ GPT 호출 함수 (신버전 API)
def call_llm(system, messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            *messages
        ],
        temperature=0.7,
        max_tokens=512
    )
    return response.choices[0].message.content

# ✅ 토론 실행
def run_debate(topic):
    system_prompt = f"너는 논리적인 토론 AI야. 주제는 '{topic}' 이고, JSON과 한글 본문을 모두 출력해."
    json_intro = '{"role":"Debater_A","turn":1,"move_type":"constructive"}'
    prompt = f"{json_intro}\n주제: {topic}에 대한 개회사를 주장-근거 형식으로 써줘."

    messages = [
        {"role": "user", "content": prompt}
    ]

    output = call_llm(system_prompt, messages)
    return output

# ✅ 출력
if start_button and topic:
    st.info(f"주제: {topic}")
    result = run_debate(topic)
    st.markdown("#### 🧠 AI 응답")
    st.write(result)
