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
# 난이도별 Python 연습 문제
# -----------------------------

BEGINNER = [
    "print('Hello World')",

    """x = 10
print(x)""",

    """name = input('이름 입력: ')
print(name)""",

    """for i in range(5):
    print(i)""",

    """numbers = [1, 2, 3]
for n in numbers:
    print(n)"""
]

INTERMEDIATE = [
    """def add(a, b):
    return a + b""",

    """for i in range(1, 10):
    if i % 2 == 0:
        print(i)""",

    """data = {'name': 'Tom', 'age': 20}

for key, value in data.items():
    print(key, value)""",

    """try:
    num = int(input())
    print(num)
except ValueError:
    print('숫자를 입력하세요')""",

    """squares = [x*x for x in range(10)]
print(squares)"""
]

ADVANCED = [
    """class Calculator:
    def add(self, a, b):
        return a + b""",

    """with open('sample.txt', 'r') as file:
    data = file.read()
    print(data)""",

    """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)""",

    """import pandas as pd

df = pd.DataFrame({
    'name': ['Tom', 'Jane'],
    'age': [20, 30]
})

print(df)""",

    """result = list(
    map(
        lambda x: x * 2,
        filter(lambda x: x % 2 == 0, range(10))
    )
)

print(result)"""
]

# -----------------------------
# 난이도 선택
# -----------------------------

difficulty = st.sidebar.selectbox(
    "난이도 선택",
    ["초급", "중급", "고급"]
)

if difficulty == "초급":
    problems = BEGINNER
elif difficulty == "중급":
    problems = INTERMEDIATE
else:
    problems = ADVANCED

# -----------------------------
# 세션 상태 초기화
# -----------------------------

if "target_code" not in st.session_state:
    st.session_state.target_code = random.choice(problems)

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "finished" not in st.session_state:
    st.session_state.finished = False

# -----------------------------
# UI
# -----------------------------

st.title("🐍 Python 코드 타자 연습")

st.markdown(f"### 현재 난이도: `{difficulty}`")

st.write("아래 Python 코드를 그대로 입력하세요.")

# 문제 코드 표시
st.code(st.session_state.target_code, language="python")

st.divider()

st.subheader("⌨ 코드 입력")

# Ace Editor 입력창
user_code = st_ace(
    placeholder="여기에 Python 코드를 입력하세요...",
    language="python",
    theme="monokai",
    key="ace_editor",
    height=300,
    auto_update=True,
    font_size=16,
    tab_size=4,
    wrap=True,
    show_gutter=True
)

# 시작 시간
if user_code and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# -----------------------------
# 정답 체크
# -----------------------------

if user_code.strip() == st.session_state.target_code.strip():

    end_time = time.time()

    elapsed = end_time - st.session_state.start_time

    total_chars = len(st.session_state.target_code)

    correct_chars = sum(
        1 for a, b in zip(user_code, st.session_state.target_code)
        if a == b
    )

    accuracy = (correct_chars / total_chars) * 100

    words = len(st.session_state.target_code.split())

    wpm = (words / elapsed) * 60

    st.success("🎉 정답입니다!")

    col1, col2, col3 = st.columns(3)

    col1.metric("⏱ 시간", f"{elapsed:.2f}초")
    col2.metric("⚡ 속도", f"{wpm:.2f} WPM")
    col3.metric("🎯 정확도", f"{accuracy:.2f}%")

    st.balloons()

    st.session_state.finished = True

# -----------------------------
# 다음 문제
# -----------------------------

if st.session_state.finished:
    if st.button("다음 문제"):
        st.session_state.target_code = random.choice(problems)
        st.session_state.start_time = None
        st.session_state.finished = False
        st.rerun()
