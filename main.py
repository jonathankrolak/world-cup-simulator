import random


teams = {
    "Argentina": 92,
    "France": 91,
    "Brazil": 90,
    "England": 89,
    "Germany": 87,
    "Spain": 87,
    "Portugal": 86,
    "USA": 78,
}


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


score_one, score_two = simulate_match("Argentina", "USA")

print(f"Argentina {score_one} - {score_two} USA")