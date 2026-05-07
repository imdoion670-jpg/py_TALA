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
    "print('Hello World')",

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

if "username" not in st.session_state:
    st.session_state.username = ""

# -----------------------------
# 사이드바
# -----------------------------

st.sidebar.title("설정")

# 이름 입력
username = st.sidebar.text_input(
    "이름",
    value=st.session_state.username
)

st.session_state.username = username

# 난이도 선택
difficulty = st.sidebar.selectbox(
    "난이도",
    list(LEVELS.keys()),
    index=list(LEVELS.keys()).index(st.session_state.difficulty)
)

# 난이도 변경 감지
if difficulty != st.session_state.difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.target_code = random.choice(
        LEVELS[difficulty]
    )
    st.session_state.start_time = None
    st.session_state.finished = False

# -----------------------------
# 메인 화면
# -----------------------------

st.title("🐍 Python 코드 타자 연습")

if username:
    st.write(f"안녕하세요, **{username}** 님 👋")

st.markdown(
    f"### 현재 난이도: `{st.session_state.difficulty}`"
)

st.write("아래 Python 코드를 그대로 입력하세요.")

# 문제 표시
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
    placeholder="Python 코드를 입력하세요...",
    language="python",
    theme="monokai",
    key=f"ace_{st.session_state.target_code}",
    height=300,
    font_size=16,
    tab_size=4,
    wrap=True,
    auto_update=True
)

# 시작 시간
if user_code and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# -----------------------------
# 정답 체크
# -----------------------------

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

    st.success("🎉 정답입니다!")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "⏱ 시간",
        f"{elapsed:.2f}초"
    )

    col2.metric(
        "⚡ 속도",
        f"{wpm:.2f} WPM"
    )

    col3.metric(
        "🎯 정확도",
        f"{accuracy:.2f}%"
    )

    st.session_state.finished = True

# -----------------------------
# 다음 문제 버튼
# -----------------------------

if st.session_state.finished:

    if st.button("다음 문제"):

        st.session_state.target_code = random.choice(
            LEVELS[st.session_state.difficulty]
        )

        st.session_state.start_time = None
        st.session_state.finished = False

        st.rerun()
