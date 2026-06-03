from group_stage import simulate_group_stage
from knockout_stage import simulate_knockout_stage


def simulate_tournament():
    advancing_teams = simulate_group_stage()
    champion = simulate_knockout_stage(advancing_teams)

    return champion