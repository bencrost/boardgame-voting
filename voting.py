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

def instant_runoff(games):
    """
    Instant Runoff Voting (IRV).

    Input:
        games = [
            [game_name, voter1_rank, voter2_rank, ...],
            ...
        ]

    Returns:
        winner, rounds

    where rounds is a list of dictionaries containing
    first-place vote counts for each round.
    """

    game_names = [row[0] for row in games]

    n_voters = len(games[0]) - 1

    # Convert game-centric data into voter ballots
    ballots = []

    for voter in range(n_voters):

        ranking = []

        for row in games:
            game = row[0]
            rank = row[voter + 1]

            ranking.append((rank, game))

        ranking.sort()

        ballots.append([game for rank, game in ranking])

    remaining = set(game_names)

    rounds = []

    while len(remaining) > 1:

        counts = {game: 0 for game in remaining}

        # Count first active preference on each ballot
        for ballot in ballots:

            for game in ballot:

                if game in remaining:
                    counts[game] += 1
                    break

        rounds.append(counts.copy())

        total_votes = sum(counts.values())

        # Check for majority winner
        for game, votes in counts.items():

            if votes > total_votes / 2:
                return game, rounds

        # Eliminate lowest vote-getter
        loser = min(counts, key=counts.get)

        remaining.remove(loser)

    winner = list(remaining)[0]

    return winner, rounds

def plurality_vote(games):
    """
    Plurality voting.

    Counts only first-place votes.

    Returns:
        winners, results

    winners is a list because there may be a tie.
    results is a sorted list: [[game_name, first_place_votes], ...]
    """

    results = []

    for row in games:
        game_name = row[0]
        rankings = row[1:]

        first_place_votes = 0

        for rank in rankings:
            if rank == 1:
                first_place_votes += 1

        results.append([game_name, first_place_votes])

    results.sort(key=lambda x: x[1], reverse=True)

    top_score = results[0][1]
    winners = [game for game, score in results if score == top_score]

    return winners, results
