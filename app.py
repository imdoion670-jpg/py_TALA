import streamlit as st
import random
import time
from streamlit_ace import st_ace

st.set_page_config(
    page_title="Python 타자 게임",
    page_icon="🐍",
    layout="wide"
)

# -----------------------------
# 문제 데이터
# -----------------------------

BEGINNER = [
    """print('Hello World')""",

    """x = 10
print(x)""",

    """for i in range(5):
    print(i)"""
]

INTERMEDIATE = [
    """def add(a, b):
    return a + b""",

    """try:
    num = int(input())
    print(num)
except ValueError:
    print('error')"""
]

ADVANCED = [
    """class Calculator:
    def add(self, a, b):
        return a + b""",

    """result = list(
    map(
        lambda x: x * 2,
        range(10)
    )
)

print(result)"""
]

LEVELS = {
    "초급": BEGINNER,
    "중급": INTERMEDIATE,
    "고급": ADVANCED
}

# -----------------------------
# 세션 상태 초기화
# -----------------------------

defaults = {
    "page": "start",
    "username": "",
    "difficulty": "초급",
    "target_code": "",
    "start_time": None,
    "result": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# 시작 화면
# -----------------------------

if st.session_state.page == "start":

    st.title("🐍 Python 코드 타자 게임")

    st.markdown("## Python 명령어 타자 연습")

    st.write("코드를 정확하고 빠르게 입력해보세요.")

    st.divider()

    username = st.text_input(
        "이름 입력",
        placeholder="이름을 입력하세요"
    )

    difficulty = st.selectbox(
        "난이도 선택",
        ["초급", "중급", "고급"]
    )

    st.divider()

    if st.button("🚀 게임 시작", use_container_width=True):

        st.session_state.username = username
        st.session_state.difficulty = difficulty

        st.session_state.target_code = random.choice(
            LEVELS[difficulty]
        )

        st.session_state.page = "game"

        st.rerun()

# -----------------------------
# 게임 화면
# -----------------------------

elif st.session_state.page == "game":

    st.title("🐍 Python 코드 타자 게임")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"👤 사용자: {st.session_state.username}")

    with col2:
        st.info(f"🎯 난이도: {st.session_state.difficulty}")

    st.divider()

    st.subheader("📌 아래 코드를 입력하세요")

    st.code(
        st.session_state.target_code,
        language="python"
    )

    st.divider()

    user_code = st_ace(
        value="",
        language="python",
        theme="monokai",
        key=f"ace_{st.session_state.target_code}",
        height=350,
        font_size=16,
        tab_size=4,
        wrap=True,
        auto_update=True,
        placeholder="여기에 Python 코드를 입력하세요..."
    )

    # 시작 시간
    if user_code and st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    # 정답 체크
    if user_code.strip() == st.session_state.target_code.strip():

        elapsed = time.time() - st.session_state.start_time

        total_chars = len(st.session_state.target_code)

        correct_chars = sum(
            1 for a, b in zip(
                user_code,
                st.session_state.target_code
            )
            if a == b
        )

        accuracy = (correct_chars / total_chars) * 100

        words = len(
            st.session_state.target_code.split()
        )

        wpm = (words / elapsed) * 60

        score = int((accuracy * wpm) / 10)

        st.session_state.result = {
            "time": elapsed,
            "accuracy": accuracy,
            "wpm": wpm,
            "score": score
        }

        st.session_state.page = "result"

        st.rerun()

# -----------------------------
# 결과 화면
# -----------------------------

elif st.session_state.page == "result":

    result = st.session_state.result

    st.title("🎉 결과 화면")

    st.success(
        f"{st.session_state.username} 님 완료!"
    )

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "⏱ 시간",
        f"{result['time']:.2f}초"
    )

    c2.metric(
        "⚡ 속도",
        f"{result['wpm']:.2f} WPM"
    )

    c3.metric(
        "🎯 정확도",
        f"{result['accuracy']:.2f}%"
    )

    c4.metric(
        "🏆 점수",
        f"{result['score']}"
    )

    st.balloons()

    st.divider()

    col1, col2 = st.columns(2)

    # 다음 문제
    with col1:

        if st.button(
            "🎲 다음 문제",
            use_container_width=True
        ):

            st.session_state.target_code = random.choice(
                LEVELS[
                    st.session_state.difficulty
                ]
            )

            st.session_state.start_time = None
            st.session_state.page = "game"

            st.rerun()

    # 처음으로
    with col2:

        if st.button(
            "🏠 처음으로",
            use_container_width=True
        ):

            st.session_state.page = "start"
            st.session_state.start_time = None

            st.rerun()
