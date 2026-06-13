import streamlit as st
import pandas as pd

from voting import borda_count, condorcet_winner
from sheets import load_ballots

sheet_id = "1fgmyIP08aw95D-qAhIkR7GiJHhDgFtp3aGTetYNaVZQ"

df = load_ballots(sheet_id)

games = df.values.tolist()

results = borda_count(games)

winner, pairwise_wins = condorcet_winner(games)

if winner is not None:
    print(f"The Condorcet winner is: {winner}")
else:
    print("There is no Condorcet winner.")

print(pairwise_wins)

st.title("Board Game Voting")

voting_system = st.selectbox(
    "Voting system",
    ["Borda", "Condorcet"]
)

if voting_system == "Borda":

    results = borda_count(games)

    winner = results[0][0]

    st.header(f"🏆 Borda winner: {winner}")

    table = pd.DataFrame(
        results,
        columns=["Game", "Borda Score"]
    )

    table.index = range(1, len(table) + 1)
    table.index.name = "Rank"

    st.dataframe(table)

elif voting_system == "Condorcet":

    winner, pairwise_wins = condorcet_winner(games)

    if winner is not None:
        st.header(f"🏆 Condorcet winner: {winner}")
    else:
        st.header("No Condorcet winner")

    table = pd.DataFrame(
        pairwise_wins.items(),
        columns=["Game", "Head-to-head wins"]
    )

    table = table.sort_values(
        "Head-to-head wins",
        ascending=False
    ).reset_index(drop=True)

    table.index = range(1, len(table) + 1)
    table.index.name = "Rank"

    st.subheader("Pairwise results")
    st.dataframe(table)

st.button("Refresh Results")
