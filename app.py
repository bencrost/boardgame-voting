import streamlit as st
import pandas as pd

from voting import borda_count, condorcet_winner, instant_runoff
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
    ["Borda", "Condorcet", "Instant Runoff", "Plurality"]
)


if voting_system == "Borda":

    st.info(
        "Borda count awards points based on ranking. "
        "Games that many people rank highly tend to perform well."
    )

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

    st.markdown("""
    ### About Borda Count

    Each player ranks all games from most preferred (1) to least preferred.

    Points are awarded based on position in each ranking. A game receives
    more points when it is ranked highly by many players.

    Borda count tends to favor games with broad support across the group,
    even if they are not everyone's first choice.
    """)

elif voting_system == "Condorcet":

    st.info(
        "A Condorcet winner is a game that would beat every other game "
        "in a head-to-head vote."
        )

    winner, pairwise_wins = condorcet_winner(games)

    if winner is not None:
        st.header(f"🏆 Condorcet winner: {winner}")
         
    else:
        st.header("There is no Condorcet winner. This makes Nicolas de Condorcet very sad")
        st.image("Nicolas_de_Condorcet.PNG", width=100)

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

    st.markdown("""
    ### About Condorcet Voting

    Every pair of games is compared head-to-head.

    If more players prefer Game A to Game B than vice versa,
    then Game A wins that matchup.

    A Condorcet winner is a game that beats every other game
    in these head-to-head comparisons.

    Condorcet voting tries to identify the option that would
    win a majority vote against any alternative.
    """)

elif voting_system == "Instant Runoff":

    winner, rounds = instant_runoff(games)

    st.header(f"🏆 Instant Runoff winner: {winner}")

    st.info(
        "Instant Runoff Voting repeatedly eliminates the game with "
        "the fewest first-place votes and transfers those votes to "
        "the next preferred remaining game."
    )

    st.subheader("Round-by-round results")

    for round_num, round_results in enumerate(rounds, start=1):

        st.markdown(f"### Round {round_num}")

        table = pd.DataFrame(
            round_results.items(),
            columns=["Game", "First-place votes"]
        )

        table = table.sort_values(
            "First-place votes",
            ascending=False
        )

        st.dataframe(
            table,
            hide_index=True
        )

elif voting_system == "Plurality":

    st.info(
        "Also known as ''First Past the Post'' - this is the most boring and uninspired of all voting systems.
        "It also opens the door to all kinds of strategic voting shenanigans and generates outcomes that nobody likes."
        "Nicolas de Condorcet judges you for selecting this abominable system."
        )

    st.image("Nicolas_de_Condorcet.PNG", width=100)

    winners, results = plurality_vote(games)

    if len(winners) == 1:
        st.header(f"🏆 Plurality winner: {winners[0]}")
    else:
        st.header("No unique plurality winner")

        tied_games = ", ".join(winners)

        st.warning(
            f"There is a tie for first place: {tied_games}. "
            "Plurality voting cannot choose a unique winner from these ballots."
        )

    table = pd.DataFrame(
        results,
        columns=["Game", "First-place votes"]
    )

    table.index = range(1, len(table) + 1)
    table.index.name = "Rank"

    st.dataframe(table)

    st.markdown("""
    ### About Plurality Voting

    Plurality voting counts only first-place votes. The game with the most
    first-place votes wins.

    With a small group and many games, ties are common because only a few
    first-place votes are available.
    """)

st.button("Refresh Results")
