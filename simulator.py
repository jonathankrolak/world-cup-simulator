from collections import defaultdict

from data import teams
from tournament import simulate_tournament


STAGE_ORDER = {
    "Round of 32": 1,
    "Round of 16": 2,
    "Quarterfinals": 3,
    "Semifinals": 4,
    "Final": 5,
    "Champion": 6,
}


def reached_stage(stage_reached, target_stage):
    if stage_reached is None:
        return False

    return STAGE_ORDER[stage_reached] >= STAGE_ORDER[target_stage]


def create_team_stats():
    team_stats = {}

    for team in teams:
        team_stats[team] = {
            "group_stage_advance": 0,
            "round_of_16": 0,
            "quarterfinals": 0,
            "semifinals": 0,
            "final": 0,
            "champion": 0,
        }

    return team_stats


def run_simulations(number_of_simulations):
    team_stats = create_team_stats()

    for simulation_number in range(number_of_simulations):
        result = simulate_tournament(show_details=False)

        stage_results = result["stage_reached"]
        champion = result["champion"]

        for team in teams:
            team_stage = stage_results.get(team)

            if reached_stage(team_stage, "Round of 32"):
                team_stats[team]["group_stage_advance"] += 1

            if reached_stage(team_stage, "Round of 16"):
                team_stats[team]["round_of_16"] += 1

            if reached_stage(team_stage, "Quarterfinals"):
                team_stats[team]["quarterfinals"] += 1

            if reached_stage(team_stage, "Semifinals"):
                team_stats[team]["semifinals"] += 1

            if reached_stage(team_stage, "Final"):
                team_stats[team]["final"] += 1

        team_stats[champion]["champion"] += 1

    print_simulation_results(team_stats, number_of_simulations)


def print_simulation_results(team_stats, number_of_simulations):
    sorted_team_stats = sorted(
        team_stats.items(),
        key=lambda team: team[1]["champion"],
        reverse=True,
    )

    print("==============================")
    print(f"World Cup Odds After {number_of_simulations} Simulations")
    print("==============================")
    print()

    header = (
        f"{'Team':<25}"
        f"{'Advance':>10}"
        f"{'R16':>10}"
        f"{'QF':>10}"
        f"{'SF':>10}"
        f"{'Final':>10}"
        f"{'Champion':>10}"
    )

    print(header)
    print("-" * len(header))

    for team, stats in sorted_team_stats:
        advance_percentage = stats["group_stage_advance"] / number_of_simulations * 100
        round_of_16_percentage = stats["round_of_16"] / number_of_simulations * 100
        quarterfinal_percentage = stats["quarterfinals"] / number_of_simulations * 100
        semifinal_percentage = stats["semifinals"] / number_of_simulations * 100
        final_percentage = stats["final"] / number_of_simulations * 100
        champion_percentage = stats["champion"] / number_of_simulations * 100

        print(
            f"{team:<25}"
            f"{advance_percentage:>9.2f}%"
            f"{round_of_16_percentage:>9.2f}%"
            f"{quarterfinal_percentage:>9.2f}%"
            f"{semifinal_percentage:>9.2f}%"
            f"{final_percentage:>9.2f}%"
            f"{champion_percentage:>9.2f}%"
        )


if __name__ == "__main__":
    run_simulations(10000)