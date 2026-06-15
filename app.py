import streamlit as st
import pandas as pd

from voting import borda_count, condorcet_winner, nanson, baldwin, plurality_vote
from sheets import load_ballots

sheet_id = "1fgmyIP08aw95D-qAhIkR7GiJHhDgFtp3aGTetYNaVZQ"

df = load_ballots(sheet_id)

games = df.values.tolist()


st.title("Board Game Voting")

voting_system = st.selectbox(
    "Voting system",
    ["Borda", "Condorcet", "Nanson", "Baldwin", "Plurality"]
)


if voting_system == "Borda":

    results = borda_count(games)

    winner = results[0][0]

    st.header(f"🏆 Borda winner: {winner}")

    st.markdown("""
    ### About Borda Count

    Each player ranks all games from most preferred to least preferred.

    Points are awarded based on position in each ranking: the lowest-ranked game in a player's ranking receives 0 points, the second lowest 1 point, etc.
    The points are then added up across all rankings and the game with the most points wins
   

    The Borda count tends to favor games with broad support across the group,
    even if they are not everyone's first choice (think Brass Birmingham, which may not be anyone's favorite game, but most people find it unobjectionable).
    """)

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
        st.header("There is no Condorcet winner. This makes Nicolas de Condorcet very sad")
        st.image("Nicolas_de_Condorcet.PNG", width=100)

    st.markdown("""
    ### About Condorcet Voting

    Every pair of games is compared head-to-head. If more voters prefer Game A to Game B than vice versa,
    then Game A wins that matchup.

    A Condorcet winner is a game that beats every other game
    in these head-to-head comparisons. The Condorcet winner is always a popular choice as there is a majority of voters that prefers it to any other game.

    Unfortunately, there is often no Condorcet winner in practice.
    In those cases, an obvious solution is to choose the game that won the most head-to-head matchups (this is called the Copeland system).
    If there's still a tie, people often use the Borda count as the tie-breaker.
    """)

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

    st.markdown("""
    ### About Plurality Voting

    Plurality voting counts only first-place votes. The game with the most
    first-place votes wins.

    "Also known as first-past-the-post, this is the most boring and uninspired of all voting systems. It opens the door to all kinds of strategic voting shenanigans and generates outcomes that nobody likes. People who think this is a good system should be ashamed of themselves - Nicolas de Condorcet judges you for even considering it."
    """)

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

    


elif voting_system == "Nanson":

    winners, rounds = nanson(games)

    if len(winners) == 1:
        st.header(f"🏆 Nanson winner: {winners[0]}")
    else:
        st.header("There is no unique Nanson winner")
        st.warning(
            "Nanson's method ended in a tie among: "
            + ", ".join(winners)
        )

    st.markdown("""
    ### About Nanson's Method

    Nanson's method combines Borda count with elimination (it thus combines features of the Borda and Instant Runoff systems).

    In each round, games receive Borda scores based only on the games still
    remaining. Any game with a below-average Borda score is eliminated.

    The process repeats until one game remains.

    Unlike ordinary Borda count, Nanson's method will select the Condorcet
    winner whenever one exists.
    """)

    st.subheader("Round-by-round results")

    for round_num, round_info in enumerate(rounds, start=1):

        st.markdown(f"### Round {round_num}")

        st.write(
            f"Average Borda score: "
            f"{round_info['average_score']:.2f}"
        )

        table = pd.DataFrame(
            round_info["scores"],
            columns=["Game", "Borda Score"]
        )

        table["Eliminated"] = table["Game"].isin(
            round_info["eliminated"]
        )

        st.dataframe(table, hide_index=True)

elif voting_system == "Baldwin":

    winners, rounds = baldwin(games)

    if len(winners) == 1:
        st.header(f"🏆 Baldwin winner: {winners[0]}")
    else:
        st.header("No unique Baldwin winner")
        st.warning(
            "The Baldwin method ended in a tie among: "
            + ", ".join(winners)
        )

    st.markdown("""
    ### About the Baldwin Method

    The Baldwin method combines Borda count with sequential elimination.

    In each round, games receive Borda scores based only on the games still
    remaining. The game with the lowest Borda score is eliminated.

    The process repeats until one game remains.

    It is similar to Nanson's method, but more gradual: Nanson can eliminate
    several below-average games in one round, while Baldwin eliminates only
    one game at a time.
    """)
    
    st.subheader("Round-by-round results")

    for round_num, round_info in enumerate(rounds, start=1):

        st.markdown(f"### Round {round_num}")

        table = pd.DataFrame(
            round_info["scores"],
            columns=["Game", "Borda Score"]
        )

        table["Eliminated"] = table["Game"].isin(
            round_info["eliminated"]
        )

        st.dataframe(table, hide_index=True)

    
    

st.button("Refresh Results")
