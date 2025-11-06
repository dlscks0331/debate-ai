import openai
import streamlit as st

# ✅ 여기에 너의 API 키 붙여넣기
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🔁 GPT 호출 함수
def call_llm(system: str, messages: list[dict], max_tokens: int = 512, temperature: float = 0.7) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            *messages
        ]
    )
    return response.choices[0].message["content"]

# 🧠 토론 로직
def run_debate(topic: str) -> list[str]:
    outputs = []
    system_prompt = f"너는 논리적인 토론 AI야. 모든 응답은 JSON 형식으로 시작하고, 이어서 사람이 읽을 수 있는 한국어 본문을 출력해.\n주제: {topic}"

    prompts = [
        {"role": "user", "content": f'{{"role":"Debater_A","turn":1,"move_type":"constructive"}}\n주제: {topic}에 대한 개회사를 주장-근거 형식으로 써줘.'},
        {"role": "user", "content": f'{{"role":"Debater_B","turn":2,"move_type":"rebuttal"}}\n위 주장을 조목조목 반박하고 질문도 덧붙여줘.'},
        {"role": "user", "content": f'{{"role":"Debater_A","turn":3,"move_type":"cross"}}\n상대에게 교차질의 2개 만들어줘.'},
        {"role": "user", "content": f'{{"role":"Judge","turn":4,"move_type":"weighing"}}\n양측 주장의 강점, 근거, 영향력 등을 비교 평가해줘.'},
        {"role": "user", "content": f'{{"role":"Debater_B","turn":5,"move_type":"closing"}}\n최종 요약과 한줄 결론 제시.'}
    ]

    for p in prompts:
        output = call_llm(system_prompt, [p])
        outputs.append(output)
    
    return outputs# 🖥️ Streamlit UI 구성
st.title("🗣️ AI 토론 생성기 (GPT-3.5)")
st.caption("OpenAI GPT를 활용한 실시간 토론 시뮬레이션")

topic = st.text_input("💡 토론 주제를 입력하세요:", "청소년의 스마트폰 사용을 제한해야 하는가")

if st.button("🎬 토론 시작"):
    with st.spinner("토론 생성 중..."):
        results = run_debate(topic)
        for i, r in enumerate(results):
            st.subheader(f"📌 단계 {i+1}")
            st.write(r)
