from match import simulate_knockout_match


def get_team_names(advancing_teams):
    team_names = []

    for team_info in advancing_teams:
        team_names.append(team_info["team"])

    return team_names


def get_round_name(number_of_teams):
    if number_of_teams == 8:
        return "Quarterfinals"
    if number_of_teams == 4:
        return "Semifinals"
    if number_of_teams == 2:
        return "Final"

    return f"Round of {number_of_teams}"


def simulate_knockout_stage(advancing_teams):
    knockout_teams = get_team_names(advancing_teams)

    print()
    print("==============================")
    print("Knockout Stage")
    print("==============================")

    while len(knockout_teams) > 1:
        round_winners = []

        print()
        round_name = get_round_name(len(knockout_teams))
        print(round_name)

        for i in range(len(knockout_teams) // 2):
            team_one = knockout_teams[i]
            team_two = knockout_teams[len(knockout_teams) - 1 - i]

            winner, team_one_goals, team_two_goals = simulate_knockout_match(
                team_one,
                team_two,
            )

            print(f"{team_one} {team_one_goals} - {team_two_goals} {team_two}")
            print(f"Winner: {winner}")

            round_winners.append(winner)

        knockout_teams = round_winners

    champion = knockout_teams[0]

    print()
    print("==============================")
    print(f"Champion: {champion}")
    print("==============================")

    return champion