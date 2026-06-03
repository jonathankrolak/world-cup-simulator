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
    "Japan": 80,
    "Mexico": 79,
}


groups = {
    "Group A": ["Argentina", "USA", "Japan", "Mexico"],
    "Group B": ["France", "Brazil", "Germany", "Portugal"],
}


def create_standings(group):
    standings = {}

    for team in group:
        standings[team] = {
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0,
        }

    return standings


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


def update_standings(standings, team_one, team_two, team_one_goals, team_two_goals):
    standings[team_one]["played"] += 1
    standings[team_two]["played"] += 1

    standings[team_one]["goals_for"] += team_one_goals
    standings[team_one]["goals_against"] += team_two_goals

    standings[team_two]["goals_for"] += team_two_goals
    standings[team_two]["goals_against"] += team_one_goals

    standings[team_one]["goal_difference"] = (
        standings[team_one]["goals_for"] - standings[team_one]["goals_against"]
    )

    standings[team_two]["goal_difference"] = (
        standings[team_two]["goals_for"] - standings[team_two]["goals_against"]
    )

    if team_one_goals > team_two_goals:
        standings[team_one]["wins"] += 1
        standings[team_two]["losses"] += 1
        standings[team_one]["points"] += 3
    elif team_two_goals > team_one_goals:
        standings[team_two]["wins"] += 1
        standings[team_one]["losses"] += 1
        standings[team_two]["points"] += 3
    else:
        standings[team_one]["draws"] += 1
        standings[team_two]["draws"] += 1
        standings[team_one]["points"] += 1
        standings[team_two]["points"] += 1


def simulate_group(group):
    standings = create_standings(group)

    print("Group Matches:\n")

    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            team_one = group[i]
            team_two = group[j]

            team_one_goals, team_two_goals = simulate_match(team_one, team_two)

            print(f"{team_one} {team_one_goals} - {team_two_goals} {team_two}")

            update_standings(
                standings,
                team_one,
                team_two,
                team_one_goals,
                team_two_goals,
            )

    return standings


def print_standings(standings):
    sorted_standings = sorted(
        standings.items(),
        key=lambda team: (
            team[1]["points"],
            team[1]["goal_difference"],
            team[1]["goals_for"],
        ),
        reverse=True,
    )

    print("\nGroup Standings:\n")

    for position, team_data in enumerate(sorted_standings, start=1):
        team_name = team_data[0]
        stats = team_data[1]

        print(
            f"{position}. {team_name} | "
            f"{stats['points']} pts | "
            f"W: {stats['wins']} "
            f"D: {stats['draws']} "
            f"L: {stats['losses']} | "
            f"GF: {stats['goals_for']} "
            f"GA: {stats['goals_against']} "
            f"GD: {stats['goal_difference']}"
        )


for group_name, group_teams in groups.items():
    print("==============================")
    print(group_name)
    print("==============================")

    standings = simulate_group(group_teams)
    print_standings(standings)

    print()