import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="토론 참여형 AI", layout="wide")

st.title("🗣️ 토론 참여형 AI (웹 MVP)")
st.write("GPT 기반 찬반 토론을 자동으로 생성합니다. 주제를 입력하고 시작해보세요!")

# ✅ 프리미엄 전환 QR 코드 UI
with st.sidebar.expander("💳 프리미엄 전환"):
    st.image("toss_qr.png", caption="토스 앱으로 스캔해 결제하기")
    st.markdown("💬 3,000원 입금 후 새로고침해주세요.")

# 주제 입력
st.markdown("---")
topic = st.text_input("🎯 토론 주제 입력", "AI는 인간 교사를 대체할 수 있는가")

# 토론 시작 버튼
if st.button("토론 시작"):

    def call_llm(system_prompt, messages, model="gpt-3.5-turbo"):
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt}] + messages,
            temperature=0.7,
            max_tokens=512
        )
        return response.choices[0].message.content

    def run_debate(topic):
        system_prompt = f"너는 논리적 토론을 주고받는 AI야. 모든 응답은 한국어로 출력해.\n주제: {topic}"

        messages = [
            {"role": "user", "content": f'{"role":"Debater_A","turn":1,"move_type":"constructive"}\n주제: {topic}에 대한 개회사를 주장-근거 형식으로 써줘.'},
            {"role": "user", "content": f'{"role":"Debater_B","turn":2,"move_type":"rebuttal"}\n위 주장을 조목조목 반박하고 질문도 덧붙여줘.'},
            {"role": "user", "content": f'{"role":"Debater_A","turn":3,"move_type":"cross"}\n상대에게 교차질의 2개 만들어줘.'},
            {"role": "user", "content": f'{"role":"Judge","turn":4,"move_type":"weighing"}\n양측 주장의 강점, 근거, 영향력 등을 비교 평가해줘.'},
            {"role": "user", "content": f'{"role":"Debater_B","turn":5,"move_type":"closing"}\n최종 요약과 한줄 결론 제시.'}
        ]

        outputs = []
        for msg in messages:
            result = call_llm(system_prompt, [msg])
            outputs.append(result)

        return outputs

    results = run_debate(topic)
    st.markdown("---")
    st.subheader("🧾 토론 결과")
    for i, section in enumerate(results):
        st.markdown(f"**[{i+1} 단계]**")
        st.write(section)
        st.markdown("---")