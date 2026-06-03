from match import simulate_knockout_match


def get_group_code(group_name):
    return group_name.replace("Group ", "")


def build_group_rankings(advancing_teams):
    group_rankings = {}

    for team_info in advancing_teams:
        group_code = get_group_code(team_info["group"])
        position = team_info["position"]

        if group_code not in group_rankings:
            group_rankings[group_code] = {}

        group_rankings[group_code][position] = team_info

    return group_rankings


def get_team(group_rankings, group_code, position):
    return group_rankings[group_code][position]["team"]


def assign_third_place_teams_to_slots(group_rankings, third_place_slots):
    qualified_third_place_teams = []

    for group_code, rankings in group_rankings.items():
        if 3 in rankings:
            qualified_third_place_teams.append(rankings[3])

    qualified_third_place_teams = sorted(
        qualified_third_place_teams,
        key=lambda team_info: (
            team_info["stats"]["points"],
            team_info["stats"]["goal_difference"],
            team_info["stats"]["goals_for"],
        ),
        reverse=True,
    )

    assignments = {}
    used_groups = set()

    # Sort slots by fewest options first so we don't trap ourselves later.
    sorted_slots = sorted(
        third_place_slots,
        key=lambda slot: len(slot["allowed_groups"]),
    )

    def backtrack(slot_index):
        if slot_index == len(sorted_slots):
            return True

        slot = sorted_slots[slot_index]
        slot_name = slot["slot_name"]
        allowed_groups = slot["allowed_groups"]

        possible_teams = []

        for team_info in qualified_third_place_teams:
            group_code = get_group_code(team_info["group"])

            if group_code in used_groups:
                continue

            if group_code in allowed_groups:
                possible_teams.append(team_info)

        for team_info in possible_teams:
            group_code = get_group_code(team_info["group"])

            assignments[slot_name] = team_info
            used_groups.add(group_code)

            if backtrack(slot_index + 1):
                return True

            used_groups.remove(group_code)
            del assignments[slot_name]

        return False

    found_valid_assignment = backtrack(0)

    if not found_valid_assignment:
        raise ValueError("Could not assign third-place teams to Round of 32 slots.")

    return assignments

def build_round_of_32_matches(advancing_teams):
    group_rankings = build_group_rankings(advancing_teams)

    third_place_slots = [
        {
            "slot_name": "Match 74 Third Place",
            "allowed_groups": ["A", "B", "C", "D", "F"],
        },
        {
            "slot_name": "Match 77 Third Place",
            "allowed_groups": ["C", "D", "F", "G", "H"],
        },
        {
            "slot_name": "Match 79 Third Place",
            "allowed_groups": ["C", "E", "F", "H", "I"],
        },
        {
            "slot_name": "Match 80 Third Place",
            "allowed_groups": ["E", "H", "I", "J", "K"],
        },
        {
            "slot_name": "Match 81 Third Place",
            "allowed_groups": ["B", "E", "F", "I", "J"],
        },
        {
            "slot_name": "Match 82 Third Place",
            "allowed_groups": ["A", "E", "H", "I", "J"],
        },
        {
            "slot_name": "Match 85 Third Place",
            "allowed_groups": ["E", "F", "G", "I", "J"],
        },
        {
            "slot_name": "Match 87 Third Place",
            "allowed_groups": ["D", "E", "I", "J", "L"],
        },
    ]

    third_place_assignments = assign_third_place_teams_to_slots(
        group_rankings,
        third_place_slots,
    )

    matches = [
        (
            "Match 73",
            get_team(group_rankings, "A", 2),
            get_team(group_rankings, "B", 2),
        ),
        (
            "Match 74",
            get_team(group_rankings, "E", 1),
            third_place_assignments["Match 74 Third Place"]["team"],
        ),
        (
            "Match 75",
            get_team(group_rankings, "F", 1),
            get_team(group_rankings, "C", 2),
        ),
        (
            "Match 76",
            get_team(group_rankings, "C", 1),
            get_team(group_rankings, "F", 2),
        ),
        (
            "Match 77",
            get_team(group_rankings, "I", 1),
            third_place_assignments["Match 77 Third Place"]["team"],
        ),
        (
            "Match 78",
            get_team(group_rankings, "E", 2),
            get_team(group_rankings, "I", 2),
        ),
        (
            "Match 79",
            get_team(group_rankings, "A", 1),
            third_place_assignments["Match 79 Third Place"]["team"],
        ),
        (
            "Match 80",
            get_team(group_rankings, "L", 1),
            third_place_assignments["Match 80 Third Place"]["team"],
        ),
        (
            "Match 81",
            get_team(group_rankings, "D", 1),
            third_place_assignments["Match 81 Third Place"]["team"],
        ),
        (
            "Match 82",
            get_team(group_rankings, "G", 1),
            third_place_assignments["Match 82 Third Place"]["team"],
        ),
        (
            "Match 83",
            get_team(group_rankings, "K", 2),
            get_team(group_rankings, "L", 2),
        ),
        (
            "Match 84",
            get_team(group_rankings, "H", 1),
            get_team(group_rankings, "J", 2),
        ),
        (
            "Match 85",
            get_team(group_rankings, "B", 1),
            third_place_assignments["Match 85 Third Place"]["team"],
        ),
        (
            "Match 86",
            get_team(group_rankings, "J", 1),
            get_team(group_rankings, "H", 2),
        ),
        (
            "Match 87",
            get_team(group_rankings, "K", 1),
            third_place_assignments["Match 87 Third Place"]["team"],
        ),
        (
            "Match 88",
            get_team(group_rankings, "D", 2),
            get_team(group_rankings, "G", 2),
        ),
    ]

    return matches


def simulate_bracket_match(match_name, team_one, team_two, show_details=True):
    winner, team_one_goals, team_two_goals, penalty_info = simulate_knockout_match(
        team_one,
        team_two,
    )

    if show_details:
        print(f"{match_name}: {team_one} {team_one_goals} - {team_two_goals} {team_two}")

        if penalty_info is not None:
            print(
                f"{penalty_info['winner']} wins "
                f"{penalty_info['team_one_penalties']} - "
                f"{penalty_info['team_two_penalties']} on penalties"
            )

        print(f"Winner: {winner}")
        print()

    return winner


def simulate_knockout_stage(advancing_teams, show_details=True):
    winners = {}

    stage_reached = {}

    for team_info in advancing_teams:
        stage_reached[team_info["team"]] = "Round of 32"

    if show_details:
        print()
        print("==============================")
        print("Knockout Stage")
        print("==============================")

        print()
        print("Round of 32")
        print("------------------------------")

    round_of_32_matches = build_round_of_32_matches(advancing_teams)

    for match_name, team_one, team_two in round_of_32_matches:
        winners[match_name] = simulate_bracket_match(
            match_name,
            team_one,
            team_two,
            show_details,
        )

        stage_reached[winners[match_name]] = "Round of 16"

    next_rounds = [
        (
            "Round of 16",
            "Quarterfinals",
            [
                ("Match 89", "Match 73", "Match 75"),
                ("Match 90", "Match 74", "Match 77"),
                ("Match 91", "Match 76", "Match 78"),
                ("Match 92", "Match 79", "Match 80"),
                ("Match 93", "Match 83", "Match 84"),
                ("Match 94", "Match 81", "Match 82"),
                ("Match 95", "Match 86", "Match 88"),
                ("Match 96", "Match 85", "Match 87"),
            ],
        ),
        (
            "Quarterfinals",
            "Semifinals",
            [
                ("Match 97", "Match 89", "Match 90"),
                ("Match 98", "Match 93", "Match 94"),
                ("Match 99", "Match 91", "Match 92"),
                ("Match 100", "Match 95", "Match 96"),
            ],
        ),
        (
            "Semifinals",
            "Final",
            [
                ("Match 101", "Match 97", "Match 98"),
                ("Match 102", "Match 99", "Match 100"),
            ],
        ),
        (
            "Final",
            "Champion",
            [
                ("Match 104", "Match 101", "Match 102"),
            ],
        ),
    ]

    for round_name, next_stage_name, matches in next_rounds:
        if show_details:
            print()
            print(round_name)
            print("------------------------------")

        for match_name, previous_match_one, previous_match_two in matches:
            team_one = winners[previous_match_one]
            team_two = winners[previous_match_two]

            winners[match_name] = simulate_bracket_match(
                match_name,
                team_one,
                team_two,
                show_details,
            )

            stage_reached[winners[match_name]] = next_stage_name

    champion = winners["Match 104"]

    if show_details:
        print("==============================")
        print(f"Champion: {champion}")
        print("==============================")

    return champion, stage_reached