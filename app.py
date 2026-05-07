import streamlit as st
import random
import time

# Python 연습 문장
sentences = [
    "print('Hello World')",
    "for i in range(10):",
    "if x > 0:",
    "def my_function():",
    "import pandas as pd",
    "list_comprehension = [x for x in range(5)]",
    "while True:",
    "try:",
    "except ValueError:",
    "class MyClass:",
    "return x * 2",
    "with open('file.txt', 'r') as f:",
]

# 세션 상태 초기화
if "target_text" not in st.session_state:
    st.session_state.target_text = random.choice(sentences)

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "finished" not in st.session_state:
    st.session_state.finished = False

st.title("🐍 Python 타자 연습 앱")

st.write("아래 Python 명령어를 그대로 입력하세요.")

# 목표 문장 표시
st.code(st.session_state.target_text, language="python")

# 입력창
user_input = st.text_input("여기에 입력하세요")

# 시작 시간 기록
if user_input and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# 결과 계산
if user_input == st.session_state.target_text:
    end_time = time.time()

    elapsed_time = end_time - st.session_state.start_time

    # 단어 수 계산
    words = len(st.session_state.target_text.split())

    # WPM 계산
    wpm = (words / elapsed_time) * 60

    # 정확도 계산
    correct_chars = sum(
        1 for a, b in zip(user_input, st.session_state.target_text) if a == b
    )

    accuracy = (correct_chars / len(st.session_state.target_text)) * 100

    st.success("정답입니다! 🎉")

    st.write(f"⏱ 시간: {elapsed_time:.2f}초")
    st.write(f"⚡ 타자 속도: {wpm:.2f} WPM")
    st.write(f"🎯 정확도: {accuracy:.2f}%")

    st.session_state.finished = True

# 다음 문제 버튼
if st.session_state.finished:
    if st.button("다음 문제"):
        st.session_state.target_text = random.choice(sentences)
        st.session_state.start_time = None
        st.session_state.finished = False
        st.rerun()
