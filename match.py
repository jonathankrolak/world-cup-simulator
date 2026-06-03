import math
import random
from data import teams


def calculate_expected_result(team_one, team_two):
    team_one_rating = teams[team_one]
    team_two_rating = teams[team_two]

    rating_difference = team_two_rating - team_one_rating

    expected_result = 1 / (10 ** (rating_difference / 600) + 1)

    return expected_result


def generate_poisson_goals(expected_goals):
    goals = 0
    probability = math.exp(-expected_goals)
    cumulative_probability = probability
    random_value = random.random()

    while random_value > cumulative_probability:
        goals += 1
        probability *= expected_goals / goals
        cumulative_probability += probability

    return goals


def calculate_expected_goals(team_one, team_two):
    team_one_expected_result = calculate_expected_result(team_one, team_two)

    rating_advantage = team_one_expected_result - 0.5

    team_one_expected_goals = 1.25 + rating_advantage
    team_two_expected_goals = 1.25 - rating_advantage

    team_one_expected_goals = max(0.4, min(2.6, team_one_expected_goals))
    team_two_expected_goals = max(0.4, min(2.6, team_two_expected_goals))

    return team_one_expected_goals, team_two_expected_goals


def simulate_match(team_one, team_two):
    team_one_expected_goals, team_two_expected_goals = calculate_expected_goals(
        team_one,
        team_two,
    )

    team_one_goals = generate_poisson_goals(team_one_expected_goals)
    team_two_goals = generate_poisson_goals(team_two_expected_goals)

    return team_one_goals, team_two_goals


def simulate_penalty_shootout(team_one, team_two):
    team_one_expected_result = calculate_expected_result(team_one, team_two)

    team_one_make_chance = 0.76 + ((team_one_expected_result - 0.5) * 0.08)
    team_two_make_chance = 0.76 + (((1 - team_one_expected_result) - 0.5) * 0.08)

    team_one_score = 0
    team_two_score = 0

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