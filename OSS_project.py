import streamlit as st
import random
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="가위바위보 게임", page_icon="✊")

st.title("✊ 가위바위보 게임")

# 사용자 입력
username = st.text_input("닉네임을 입력하세요")
difficulty = st.selectbox("AI 난이도를 선택하세요", ["학부생", "석박사", "교수님"])
choices = ["가위", "바위", "보"]

if username:
    col1, col2, col3 = st.columns(3)
    user_choice = None
    if col1.button("✌ 가위"): user_choice = "가위"
    if col2.button("✊ 바위"): user_choice = "바위"
    if col3.button("✋ 보"): user_choice = "보"

    if user_choice:
        # AI 선택
        if difficulty == "Easy":
            ai_choice = random.choice(choices)
        elif difficulty == "Normal":
            weights = [0.33, 0.34, 0.33]
            ai_choice = random.choices(choices, weights=weights)[0]
        else:  # Cheater
            counter = {"가위": "바위", "바위": "보", "보": "가위"}
            ai_choice = counter[user_choice]

        # 결과 판정
        if user_choice == ai_choice:
            result = "무승부"
        elif (user_choice == "가위" and ai_choice == "보") or \
             (user_choice == "바위" and ai_choice == "가위") or \
             (user_choice == "보" and ai_choice == "바위"):
            result = "승"
        else:
            result = "패"

        # 결과 출력
        st.subheader(f"🎮 결과: 당신은 **{result}**!")
        st.write(f"당신의 선택: {user_choice} | AI({difficulty})의 선택: {ai_choice}")

        # 기록 저장
        record = pd.DataFrame([{
            "사용자": username,
            "선택": user_choice,
            "AI 선택": ai_choice,
            "결과": result,
            "난이도": difficulty,
            "날짜": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        file = "records.csv"
        if os.path.exists(file):
            record.to_csv(file, mode="a", header=False, index=False, encoding="utf-8-sig")
        else:
            record.to_csv(file, index=False, encoding="utf-8-sig")

# 전적 출력
st.markdown("---")
st.subheader("📊 나의 전적")
if username and os.path.exists("records.csv"):
    df = pd.read_csv("records.csv", encoding="utf-8-sig")
    st.dataframe(df[df["사용자"] == username])

st.markdown("---")
st.subheader("🏆 전체 승률 랭킹 Top 5")
if os.path.exists("records.csv"):
    df = pd.read_csv("records.csv", encoding="utf-8-sig")
    wins = df[df["결과"] == "승"].groupby("사용자").size()
    total = df.groupby("사용자").size()
    ranking = (wins / total * 100).fillna(0).round(1).reset_index()
    ranking.columns = ["사용자", "승률(%)"]
    ranking = ranking.sort_values("승률(%)", ascending=False).head(5)
    st.dataframe(ranking)
