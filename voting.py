def borda_count(games):

    n_games = len(games)
    results = []

    for row in games:

        game_name = row[0]
        rankings = row[1:]

        score = 0

        for rank in rankings:
            score += n_games - rank

        results.append([game_name, score])

    results.sort(key=lambda x: x[1], reverse=True)

    return results

def condorcet_winner(games):
    """
    Finds the Condorcet winner, if one exists.

    A Condorcet winner is a game that beats every other game
    in head-to-head pairwise comparisons.

    Returns:
        [winner_name, pairwise_wins]

    If no Condorcet winner exists, returns:
        [None, pairwise_wins]
    """

    game_names = [row[0] for row in games]
    rankings = {row[0]: row[1:] for row in games}

    pairwise_wins = {}

    for game_a in game_names:

        wins = 0

        for game_b in game_names:

            if game_a == game_b:
                continue

            votes_for_a = 0
            votes_for_b = 0

            for rank_a, rank_b in zip(rankings[game_a], rankings[game_b]):

                if rank_a < rank_b:
                    votes_for_a += 1
                elif rank_b < rank_a:
                    votes_for_b += 1

            if votes_for_a > votes_for_b:
                wins += 1

        pairwise_wins[game_a] = wins

    n_games = len(game_names)

    for game, wins in pairwise_wins.items():
        if wins == n_games - 1:
            return [game, pairwise_wins]

    return [None, pairwise_wins]
