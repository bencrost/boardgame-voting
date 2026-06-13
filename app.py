import streamlit as st

from voting import borda_count
from sheets import load_ballots

sheet_id = "1fgmyIP08aw95D-qAhIkR7GiJHhDgFtp3aGTetYNaVZQ"

df = load_ballots(sheet_id)

games = df.values.tolist()

results = borda_count(games)

st.title("Board Game Voting")

winner = results[0][0]

st.header(f"🏆 Winner: {winner}")

for rank, (game, score) in enumerate(results, start=1):
    st.write(f"{rank}. {game} ({score} points)")
