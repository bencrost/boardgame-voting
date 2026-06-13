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
