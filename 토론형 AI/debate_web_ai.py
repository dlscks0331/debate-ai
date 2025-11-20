import streamlit as st
import openai
import os

# API 키 설정 (환경 변수 또는 직접 입력)
openai.api_key = os.getenv("OPENAI_API_KEY")

# LLM 호출 함수
def call_llm(role, turn, move_type, content):
    system = "너는 논리적이고 명확한 주장을 펼치는 토론 AI야. 모든 응답은 사람이 읽기 쉽게 한국어로 해."
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f'{content}'}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=512
    )
    return response.choices[0].message.content

# Streamlit UI
st.set_page_config(page_title="AI 토론 챗봇", layout="centered")
st.title("🗣️ AI 토론 챗봇")

# 프리미엄 여부 기본값
paid = False

# 사이드바 - 프리미엄 전환 UI
with st.sidebar:
    st.markdown("## 💎 프리미엄 후원하기")
    if st.button("💸 프리미엄 전환"):
        st.image("assets/toss_qr.png", caption="토스 후원 QR", width=250)
        st.info("QR 결제를 완료하셨다면 아래 체크박스를 눌러주세요.")

    paid = st.checkbox("✅ 후원 완료했어요!")

# 주제 입력
st.markdown("### 📌 토론 주제를 입력하세요")
topic = st.text_input("예: AI는 인간 교사를 대체할 수 있는가")

if st.button("토론 시작") and topic:
    st.success("✅ 토론을 시작합니다!")

    # 개회사
    st.subheader("[1] 찬성 측 개회사")
    intro = call_llm("Debater_A", 1, "constructive", f'{"role":"Debater_A","turn":1,"move_type":"constructive"}\n주제: {topic}에 대한 개회사를 주장-근거 형식으로 써줘.')
    st.write(intro)

    # 반박
    st.subheader("[2] 반대 측 반박")
    rebuttal = call_llm("Debater_B", 2, "rebuttal", f'{"role":"Debater_B","turn":2,"move_type":"rebuttal"}\n위 주장을 조목조목 반박하고 질문도 덧붙여줘.')
    st.write(rebuttal)

    # 교차질의
    st.subheader("[3] 찬성 측 교차질의")
    cross = call_llm("Debater_A", 3, "cross", f'{"role":"Debater_A","turn":3,"move_type":"cross"}\n상대에게 교차질의 2개 만들어줘.')
    st.write(cross)

    # 평가
    st.subheader("[4] 심판의 평가")
    judge = call_llm("Judge", 4, "weighing", f'{"role":"Judge","turn":4,"move_type":"weighing"}\n양측 주장의 강점, 근거, 영향력 등을 비교 평가해줘.')
    st.write(judge)

    # 마무리
    st.subheader("[5] 반대 측 마무리")
    closing = call_llm("Debater_B", 5, "closing", f'{"role":"Debater_B","turn":5,"move_type":"closing"}\n최종 요약과 한줄 결론 제시.')
    st.write(closing)

    # 프리미엄 표시
    if paid:
        st.success("🎉 프리미엄 모드가 활성화되었습니다! 감사합니다.")
    else:
        st.warning("🔒 프리미엄 모드가 꺼져 있습니다. 사이드바에서 후원을 진행해주세요.")

elif st.button("토론 시작"):
    st.error("❗ 토론 주제를 먼저 입력해주세요.")
