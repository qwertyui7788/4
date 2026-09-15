import streamlit as st
import random
import time

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="🎰 Lucky Spin",
    page_icon="🎰",
    layout="centered"
)

# -----------------------------
# 슬롯 설정
# -----------------------------
SYMBOLS = ["🍒", "🍋", "🍊", "🍇", "🔔", "💎", "7️⃣"]

# 심볼별 배당
PAYOUTS = {
    "🍒": 5,
    "🍋": 5,
    "🍊": 8,
    "🍇": 10,
    "🔔": 15,
    "💎": 30,
    "7️⃣": 100
}

STARTING_COINS = 100


# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "coins" not in st.session_state:
    st.session_state.coins = STARTING_COINS

if "bet" not in st.session_state:
    st.session_state.bet = 10

if "reels" not in st.session_state:
    st.session_state.reels = ["❔", "❔", "❔"]

if "message" not in st.session_state:
    st.session_state.message = "🎰 행운을 시험해보세요!"

if "spins" not in st.session_state:
    st.session_state.spins = 0

if "wins" not in st.session_state:
    st.session_state.wins = 0

if "biggest_win" not in st.session_state:
    st.session_state.biggest_win = 0


# -----------------------------
# 게임 함수
# -----------------------------
def spin():
    bet = st.session_state.bet

    # 베팅 금액 확인
    if bet <= 0:
        st.session_state.message = "❌ 베팅 금액은 1 이상이어야 합니다."
        return

    if bet > st.session_state.coins:
        st.session_state.message = "💸 코인이 부족합니다!"
        return

    # 베팅 차감
    st.session_state.coins -= bet
    st.session_state.spins += 1

    # 슬롯 결과 생성
    reels = [
        random.choice(SYMBOLS),
        random.choice(SYMBOLS),
        random.choice(SYMBOLS)
    ]

    st.session_state.reels = reels

    # 결과 계산
    if reels[0] == reels[1] == reels[2]:
        multiplier = PAYOUTS[reels[0]]
        win = bet * multiplier

        st.session_state.coins += win
        st.session_state.wins += 1

        if win > st.session_state.biggest_win:
            st.session_state.biggest_win = win

        if reels[0] == "7️⃣":
            st.session_state.message = (
                f"🎉🎉 JACKPOT!!! 🎉🎉\n\n"
                f"💰 +{win} 코인!"
            )
        else:
            st.session_state.message = (
                f"🎊 대박! 3개 일치!\n\n"
                f"💰 +{win} 코인!"
            )

    # 두 개 일치
    elif reels[0] == reels[1] or reels[1] == reels[2] or reels[0] == reels[2]:
        win = bet * 2
        st.session_state.coins += win

        if win > st.session_state.biggest_win:
            st.session_state.biggest_win = win

        st.session_state.message = (
            f"✨ 2개 일치!\n\n"
            f"💰 +{win} 코인!"
        )

    else:
        st.session_state.message = "😢 아쉽네요... 다시 돌려보세요!"


def reset_game():
    st.session_state.coins = STARTING_COINS
    st.session_state.bet = 10
    st.session_state.reels = ["❔", "❔", "❔"]
    st.session_state.message = "🎰 새로운 게임을 시작합니다!"
    st.session_state.spins = 0
    st.session_state.wins = 0
    st.session_state.biggest_win = 0


# -----------------------------
# CSS
# -----------------------------
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #999;
        margin-bottom: 30px;
    }

    .slot-box {
        background: linear-gradient(145deg, #191919, #303030);
        border: 4px solid #FFD700;
        border-radius: 25px;
        padding: 25px;
        box-shadow:
            0 0 20px rgba(255, 215, 0, 0.35),
            inset 0 0 20px rgba(255,255,255,0.05);
        margin: 20px 0;
    }

    .reel {
        background: white;
        color: black;
        border-radius: 15px;
        text-align: center;
        font-size: 60px;
        padding: 15px 5px;
        min-height: 100px;
        box-shadow: inset 0 0 10px #777;
    }

    .message {
        text-align: center;
        background: #111;
        border-radius: 15px;
        padding: 18px;
        font-size: 22px;
        font-weight: bold;
        white-space: pre-line;
        margin: 20px 0;
    }

    .coin {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        color: #FFD700;
    }

    .jackpot {
        color: #ff3366;
        font-weight: 900;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# 제목
# -----------------------------
st.markdown(
    '<div class="main-title">🎰 LUCKY SPIN 🎰</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">가상 코인으로 즐기는 미니 슬롯머신</div>',
    unsafe_allow_html=True
)


# -----------------------------
# 코인 표시
# -----------------------------
st.markdown(
    f'<div class="coin">🪙 {st.session_state.coins:,} COINS</div>',
    unsafe_allow_html=True
)


# -----------------------------
# 슬롯 화면
# -----------------------------
st.markdown('<div class="slot-box">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f'<div class="reel">{st.session_state.reels[0]}</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div class="reel">{st.session_state.reels[1]}</div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<div class="reel">{st.session_state.reels[2]}</div>',
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# 결과 메시지
# -----------------------------
st.markdown(
    f'<div class="message">{st.session_state.message}</div>',
    unsafe_allow_html=True
)


# -----------------------------
# 베팅 설정
# -----------------------------
st.subheader("💰 베팅")

st.session_state.bet = st.number_input(
    "베팅할 코인",
    min_value=1,
    max_value=max(1, st.session_state.coins),
    value=min(st.session_state.bet, max(1, st.session_state.coins)),
    step=5
)


# -----------------------------
# 버튼
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button(
        "🎰 SPIN!",
        use_container_width=True,
        type="primary"
    ):
        spin()
        st.rerun()

with col2:
    if st.button(
        "🔄 게임 초기화",
        use_container_width=True
    ):
        reset_game()
        st.rerun()


# -----------------------------
# 통계
# -----------------------------
st.divider()

st.subheader("📊 게임 통계")

stat1, stat2, stat3 = st.columns(3)

with stat1:
    st.metric("🎰 스핀", st.session_state.spins)

with stat2:
    st.metric("🏆 승리", st.session_state.wins)

with stat3:
    st.metric("💎 최대 당첨", st.session_state.biggest_win)


# -----------------------------
# 배당표
# -----------------------------
st.divider()

st.subheader("🎯 배당표")

payout_data = [
    ("🍒", "3개", "5배"),
    ("🍋", "3개", "5배"),
    ("🍊", "3개", "8배"),
    ("🍇", "3개", "10배"),
    ("🔔", "3개", "15배"),
    ("💎", "3개", "30배"),
    ("7️⃣", "3개", "100배 JACKPOT"),
    ("✨", "2개", "2배"),
]

for symbol, condition, reward in payout_data:
    st.write(f"{symbol} **{condition}** → **{reward}**")


# -----------------------------
# 게임 설명
# -----------------------------
st.divider()

with st.expander("ℹ️ 게임 방법"):
    st.write(
        """
        1. 베팅할 코인을 선택합니다.
        2. **SPIN!** 버튼을 누릅니다.
        3. 같은 그림이 2개 나오면 2배!
        4. 같은 그림이 3개 나오면 심볼별 배당을 받습니다.
        5. 7️⃣ 3개가 나오면 **100배 JACKPOT!**

        이 게임의 코인은 실제 현금이나 환전 기능이 없는
        게임용 가상 코인입니다.
        """
    )
