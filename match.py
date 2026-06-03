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


def simulate_knockout_match(team_one, team_two):
    team_one_goals, team_two_goals = simulate_match(team_one, team_two)

    if team_one_goals > team_two_goals:
        return team_one, team_one_goals, team_two_goals

    if team_two_goals > team_one_goals:
        return team_two, team_one_goals, team_two_goals

    team_one_rating = teams[team_one]
    team_two_rating = teams[team_two]

    team_one_chance = team_one_rating / (team_one_rating + team_two_rating)

    winner = random.choices(
        [team_one, team_two],
        weights=[team_one_chance, 1 - team_one_chance],
        k=1,
    )[0]

    return winner, team_one_goals, team_two_goals