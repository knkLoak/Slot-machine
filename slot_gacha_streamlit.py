# slot_gacha_app.py
import streamlit as st
import pandas as pd
import random

# -------------------------
# SYMBOL SETUP
# -------------------------
symbols = [
    {"name": "🍒 Cherry", "rarity": "Common", "weight": 0.4, "payout": 5},
    {"name": "🍋 Lemon", "rarity": "Common", "weight": 0.3, "payout": 8},
    {"name": "🔔 Bell", "rarity": "Rare", "weight": 0.15, "payout": 15},
    {"name": "💎 Diamond", "rarity": "Rare", "weight": 0.1, "payout": 25},
    {"name": "7️⃣ Seven", "rarity": "Epic", "weight": 0.04, "payout": 50},
    {"name": "🎰 Jackpot", "rarity": "Legendary", "weight": 0.01, "payout": 100}
]

symbol_list = [s["name"] for s in symbols]
weights = [s["weight"] for s in symbols]
payout_dict = {s["name"]: s["payout"] for s in symbols}
rarity_dict = {s["name"]: s["rarity"] for s in symbols}

# -------------------------
# APP STATE
# -------------------------
if "spin_log" not in st.session_state:
    st.session_state.spin_log = []

# -------------------------
# FUNCTIONS
# -------------------------
def spin():
    result = random.choices(symbol_list, weights=weights, k=3)
    payout = calculate_payout(result)
    st.session_state.spin_log.append({
        "Symbols": " ".join(result),
        "Rarities": ", ".join([rarity_dict[r] for r in result]),
        "Payout": payout
    })

def simulate_spins(n):
    for _ in range(n):
        spin()

def calculate_payout(symbols):
    if len(set(symbols)) == 1:
        return payout_dict[symbols[0]]
    return 0

# -------------------------
# UI
# -------------------------
st.title("🎰 Gacha Slot Machine")

st.markdown("Spin the reels and track your session stats! Matching 3 symbols yields a payout.")

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🎯 Spin Once"):
        spin()

with col2:
    if st.button("🎲 Simulate 50 Spins"):
        simulate_spins(50)

with col3:
    if st.button("🔄 Reset Session"):
        st.session_state.spin_log = []

# Display stats if spins exist
if st.session_state.spin_log:
    df = pd.DataFrame(st.session_state.spin_log)
    total_spins = len(df)
    total_payout = df["Payout"].sum()
    rtp = (total_payout / (total_spins * 1)) * 100  # assuming 1 coin bet per spin

    st.markdown("---")
    st.subheader("📊 Spin Log")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("📈 Session Stats")
    st.markdown(f"**Total Spins:** {total_spins}")
    st.markdown(f"**Total Payout:** {total_payout}")
    st.markdown(f"**Estimated RTP:** {rtp:.2f}%")

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Spin Log (CSV)", data=csv, file_name="spin_log.csv", mime="text/csv")

    with st.expander("🧠 How the Math Works"):
        st.markdown("""
        **RTP (Return to Player):**

        \[
        RTP = \frac{\text{Total Payout}}{\text{Total Spins} \times \text{Bet Per Spin}} \times 100
        \]

        **Current Bet Per Spin:** 1 coin  
        **Payout Rule:** Only 3 identical symbols award a payout.  
        **Symbol Payouts:**
        - 🍒 Cherry: 5 coins
        - 🍋 Lemon: 8 coins
        - 🔔 Bell: 15 coins
        - 💎 Diamond: 25 coins
        - 7️⃣ Seven: 50 coins
        - 🎰 Jackpot: 100 coins
        """)
else:
    st.info("Click spin to start playing!")
