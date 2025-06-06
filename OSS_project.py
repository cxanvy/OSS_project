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

# AI 승리/무/패 매핑
win_choice = {"가위": "바위", "바위": "보", "보": "가위"}
lose_choice = {"가위": "보", "바위": "가위", "보": "바위"}

if username:
    col1, col2, col3 = st.columns(3)
    user_choice = None

    if os.path.exists("records.csv"):
        if st.button("전적 리셋"):
            df = pd.read_csv("records.csv", encoding="utf-8-sig")
            df = df[df["사용자"] != username]  # 현재 사용자 제외
            df.to_csv("records.csv", index=False, encoding="utf-8-sig")
            st.success(f"{username}님의 전적이 초기화되었습니다.")

    if col1.button("✌ 가위"):
        user_choice = "가위"
    if col2.button("✊ 바위"):
        user_choice = "바위"
    if col3.button("✋ 보"):
        user_choice = "보"

    if user_choice:
        # 난이도별 AI 선택 확률 설정
        if difficulty == "학부생":
            weights = [0.15, 0.15, 0.7]  # 승 / 무 / 패
        elif difficulty == "석박사":
            weights = [0.3, 0.3, 0.4]
        else:  # 교수님
            weights = [0.8, 0.05, 0.15]

        ai_options = [win_choice[user_choice], user_choice, lose_choice[user_choice]]
        ai_choice = random.choices(ai_options, weights=weights)[0]

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

        # 결과 저장
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

# 사용자 전적 출력
st.markdown("---")
st.subheader("📊 나의 전적")
if username and os.path.exists("records.csv"):
    df = pd.read_csv("records.csv", encoding="utf-8-sig")
    st.dataframe(df[df["사용자"] == username])

# 전체 승률 랭킹
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
