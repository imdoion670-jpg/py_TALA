import streamlit as st
import random
import time
from streamlit_ace import st_ace

st.set_page_config(
    page_title="Python 타자 연습",
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
# 세션 상태
# -----------------------------

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "초급"

if "target_code" not in st.session_state:
    st.session_state.target_code = random.choice(
        LEVELS[st.session_state.difficulty]
    )

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "finished" not in st.session_state:
    st.session_state.finished = False

# -----------------------------
# 상단 UI
# -----------------------------

st.title("🐍 Python 코드 타자 연습")

col1, col2, col3 = st.columns([2, 2, 1])

# 이름 입력
with col1:
    username = st.text_input(
        "이름 입력",
        placeholder="이름을 입력하세요"
    )

# 난이도 선택
with col2:

    difficulty = st.selectbox(
        "난이도 선택",
        ["초급", "중급", "고급"],
        index=["초급", "중급", "고급"].index(
            st.session_state.difficulty
        )
    )

    # 난이도 변경 감지
    if difficulty != st.session_state.difficulty:

        st.session_state.difficulty = difficulty

        st.session_state.target_code = random.choice(
            LEVELS[difficulty]
        )

        st.session_state.finished = False
        st.session_state.start_time = None

        st.rerun()

# 다음 문제 버튼
with col3:
    st.write("")
    st.write("")

    if st.button("🎲 다음 문제"):

        st.session_state.target_code = random.choice(
            LEVELS[st.session_state.difficulty]
        )

        st.session_state.finished = False
        st.session_state.start_time = None

        st.rerun()

# -----------------------------
# 안내
# -----------------------------

if username:
    st.success(f"{username} 님 환영합니다 👋")

st.markdown(
    f"### 현재 난이도: `{st.session_state.difficulty}`"
)

st.write("아래 Python 코드를 그대로 입력하세요.")

# 문제 코드
st.code(
    st.session_state.target_code,
    language="python"
)

st.divider()

# -----------------------------
# 코드 입력창
# -----------------------------

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

# -----------------------------
# 시작 시간
# -----------------------------

if user_code and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# -----------------------------
# 정답 판정
# -----------------------------

if user_code.strip() == st.session_state.target_code.strip():

    elapsed = time.time() - st.session_state.start_time

    chars = len(st.session_state.target_code)

    correct = sum(
        1 for a, b in zip(
            user_code,
            st.session_state.target_code
        )
        if a == b
    )

    accuracy = (correct / chars) * 100

    words = len(
        st.session_state.target_code.split()
    )

    wpm = (words / elapsed) * 60

    st.success("🎉 정답입니다!")

    c1, c2, c3 = st.columns(3)

    c1.metric("⏱ 시간", f"{elapsed:.2f}초")
    c2.metric("⚡ 속도", f"{wpm:.2f} WPM")
    c3.metric("🎯 정확도", f"{accuracy:.2f}%")

    st.balloons()
