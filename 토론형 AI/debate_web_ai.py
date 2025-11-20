import streamlit as st
import openai
import os

# ✅ OpenAI 키 불러오기 (환경변수에서)
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="토론 참여형 AI", page_icon="🤖")
st.title("🗣️ 토론 참여형 AI")
st.write("주제를 입력하면 AI가 찬반 토론을 벌입니다.")

# ✅ 사용자 입력
topic = st.text_input("토론 주제를 입력하세요", "AI는 인간 교사를 대체할 수 있는가")

# ✅ 토론 버튼
if st.button("토론 시작"):
    with st.spinner("토론 생성 중..."):
        # 시스템 프롬프트
        system_prompt = f"""
        너는 논리적인 토론에 참여하는 AI야. 역할은 찬성측 Debater_A, 반대측 Debater_B, 그리고 심판 Judge가 있어.
        응답은 JSON 형식 설명 없이 바로 시작하고, 이어서 사람이 읽을 수 있는 한국어 텍스트로 주장·반박을 보여줘.
        주제: {topic}
        """

        def call_llm(role, turn, move_type, message):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f'{{"role":"{role}","turn":{turn},"move_type":"{move_type}"}}\n{message}'}
                ],
                temperature=0.7,
                max_tokens=700
            )
            return response.choices[0].message.content

        st.subheader("1️⃣ 개회사 (찬성)")
        st.write(call_llm("Debater_A", 1, "constructive", f"{topic}에 대한 찬성 입장의 주장과 근거를 설명해줘."))

        st.subheader("2️⃣ 반박 (반대)")
        st.write(call_llm("Debater_B", 2, "rebuttal", "위 주장에 조목조목 반박하고 질문도 추가해줘."))

        st.subheader("3️⃣ 교차질의 (찬성)")
        st.write(call_llm("Debater_A", 3, "cross", "상대에게 교차질의 2개를 만들어줘."))

        st.subheader("4️⃣ 평가 및 판정 (Judge)")
        st.write(call_llm("Judge", 4, "weighing", "양측의 주장 강점, 근거, 설득력 등을 종합 평가해줘."))

        st.subheader("5️⃣ 최종 요약 (반대)")
        st.write(call_llm("Debater_B", 5, "closing", "최종 요약과 한줄 결론을 제시해줘."))

# ✅ 사이드바 - 프리미엄 후원
with st.sidebar:
    st.markdown("## 💎 프리미엄 후원하기")
    if st.button("💸 프리미엄 전환"):
        st.success("감사합니다! 아래 QR로 후원해주세요.")
        st.image("assets/toss_qr.png", caption="QR 결제 (토스)", width=250)
