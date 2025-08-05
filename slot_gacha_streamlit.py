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
prob_dict = {s["name"]: s["weight"] for s in symbols}

if "spin_log" not in st.session_state:
    st.session_state.spin_log = []
if "balance" not in st.session_state:
    st.session_state.balance = 100.00

BET_AMOUNT = 1.00

def spin():
    if st.session_state.balance < BET_AMOUNT:
        st.warning("Insufficient balance to spin.")
        return
    result = random.choices(symbol_list, weights=weights, k=3)
    payout = calculate_payout(result)
    st.session_state.balance -= BET_AMOUNT
    st.session_state.balance += payout
    st.session_state.spin_log.append({
        "Symbols": " ".join(result),
        "Rarities": ", ".join([rarity_dict[r] for r in result]),
        "Payout ($)": f"{payout:.2f}"
    })

def simulate_spins(n):
    for _ in range(n):
        spin()

def calculate_payout(symbols):
    if len(set(symbols)) == 1:
        return payout_dict[symbols[0]]
    return 0.0
    
def simulate_spins(n):
    for _ in range(n):
        spin()

def calculate_payout(symbols):
    if len(set(symbols)) == 1:
        return payout_dict[symbols[0]]
    return 0.0

st.title("Slot Machine Simulation")

st.markdown("Spin the reels and track your session stats! Matching 3 symbols yields a payout.")

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if st.button("Spin Once"):
        spin()

with col2:
    if st.button("Simulate 50 Spins"):
        simulate_spins(50)

with col3:
    if st.button("🔄 Reset Session"):
        st.session_state.spin_log = []
        st.session_state.balance = 100.00

with col4:
    if st.button("Refill Balance ($100)"):
        st.session_state.balance += 100.00
# Display stats if spins exist
if st.session_state.spin_log:
    df = pd.DataFrame(st.session_state.spin_log)
    total_spins = len(df)
    total_payout = sum([float(p.replace("$", "")) for p in df["Payout ($)"]])
    total_spent = total_spins * BET_AMOUNT
    rtp = (total_payout / total_spent) * 100 if total_spent > 0 else 0.0
    net_gain = st.session_state.balance - 100.00

    st.markdown("---")
    st.subheader("📊 Spin Log")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("📈 Session Stats")
    st.markdown(f"**Total Spins:** {total_spins}")
    st.markdown(f"**Total Spent:** ${total_spent:.2f}")
    st.markdown(f"**Total Payout:** ${total_payout:.2f}")
    st.markdown(f"**Net Gain/Loss:** ${net_gain:.2f}")
    st.markdown(f"**Estimated RTP (Return To Player):** {rtp:.2f}%")
    st.markdown(f"**Remaining Balance:** ${st.session_state.balance:.2f}")

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Spin Log (CSV)", data=csv, file_name="spin_log.csv", mime="text/csv")

    with st.expander("🧠 How the Math Works"):
        st.markdown("""
        ### RTP (Return to Player)
        $$
        RTP = \frac{\text{Total Payout}}{\text{Total Spent}} \times 100
        $$

        **Bet Per Spin:** $1.00  
        **Payout Rule:** Only 3 identical symbols award a payout.  

        ### Probabilities and Payouts
        """)
        st.table(pd.DataFrame([{"Symbol": s["name"], "Probability": s["weight"], "Payout ($)": s["payout"]} for s in symbols]))

        st.markdown("""
        ### Theoretical Expected Value (EV)
        $$
        EV = \sum (p_i^3 \times \text{payout}_i)
        $$
        Where $p_i$ is the probability of each symbol. This reflects the long-term average return per spin under ideal randomness.
        """)
else:
    st.info("Click spin to start playing!")
