from group_stage import simulate_group_stage
from knockout_stage import simulate_knockout_stage


def simulate_tournament(show_details=True):
    advancing_teams = simulate_group_stage(show_details)
    champion, stage_reached = simulate_knockout_stage(advancing_teams, show_details)

    tournament_result = {
        "champion": champion,
        "stage_reached": stage_reached,
        "advancing_teams": advancing_teams,
    }

    return tournament_result