import random
from data import teams


def simulate_match(team_one, team_two):
    team_one_rating = teams[team_one]
    team_two_rating = teams[team_two]

    team_one_goals = random.randint(0, 3)
    team_two_goals = random.randint(0, 3)

    if team_one_rating > team_two_rating:
        team_one_goals += random.choice([0, 0, 1])
    elif team_two_rating > team_one_rating:
        team_two_goals += random.choice([0, 0, 1])

    return team_one_goals, team_two_goals

def simulate_penalty_shootout(team_one, team_two):
    team_one_rating = teams[team_one]
    team_two_rating = teams[team_two]

    team_one_score = 0
    team_two_score = 0

    team_one_make_chance = 0.72 + ((team_one_rating - team_two_rating) / 1000)
    team_two_make_chance = 0.72 + ((team_two_rating - team_one_rating) / 1000)

    for shot in range(5):
        if random.random() < team_one_make_chance:
            team_one_score += 1

        if random.random() < team_two_make_chance:
            team_two_score += 1

    while team_one_score == team_two_score:
        if random.random() < team_one_make_chance:
            team_one_score += 1

        if random.random() < team_two_make_chance:
            team_two_score += 1

    winner = team_one if team_one_score > team_two_score else team_two

    return winner, team_one_score, team_two_score

def simulate_knockout_match(team_one, team_two):
    team_one_goals, team_two_goals = simulate_match(team_one, team_two)

    if team_one_goals > team_two_goals:
        return team_one, team_one_goals, team_two_goals, None

    if team_two_goals > team_one_goals:
        return team_two, team_one_goals, team_two_goals, None

    penalty_winner, team_one_penalties, team_two_penalties = simulate_penalty_shootout(
        team_one,
        team_two,
    )

    penalty_info = {
        "winner": penalty_winner,
        "team_one_penalties": team_one_penalties,
        "team_two_penalties": team_two_penalties,
    }

    return penalty_winner, team_one_goals, team_two_goals, penalty_info