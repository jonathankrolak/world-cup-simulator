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

    results = build_results_table(team_stats, number_of_simulations)

    return results


def build_results_table(team_stats, number_of_simulations):
    results = []

    for team, stats in team_stats.items():
        result = {
            "team": team,
            "advance_percentage": stats["group_stage_advance"] / number_of_simulations * 100,
            "round_of_16_percentage": stats["round_of_16"] / number_of_simulations * 100,
            "quarterfinal_percentage": stats["quarterfinals"] / number_of_simulations * 100,
            "semifinal_percentage": stats["semifinals"] / number_of_simulations * 100,
            "final_percentage": stats["final"] / number_of_simulations * 100,
            "champion_percentage": stats["champion"] / number_of_simulations * 100,
            "championships_won": stats["champion"],
        }

        results.append(result)

    results = sorted(
        results,
        key=lambda team: team["champion_percentage"],
        reverse=True,
    )

    return results


def print_simulation_results(results, number_of_simulations):
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

    for result in results:
        print(
            f"{result['team']:<25}"
            f"{result['advance_percentage']:>9.2f}%"
            f"{result['round_of_16_percentage']:>9.2f}%"
            f"{result['quarterfinal_percentage']:>9.2f}%"
            f"{result['semifinal_percentage']:>9.2f}%"
            f"{result['final_percentage']:>9.2f}%"
            f"{result['champion_percentage']:>9.2f}%"
        )


if __name__ == "__main__":
    number_of_simulations = 10000
    results = run_simulations(number_of_simulations)
    print_simulation_results(results, number_of_simulations)