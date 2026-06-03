import csv


def load_teams(file_path):
    teams = {}

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            team_name = row["team"]
            rating = float(row["rating"])

            teams[team_name] = rating

    return teams


def load_groups(file_path):
    groups = {}

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            group_name = row["group"]
            team_name = row["team"]

            if group_name not in groups:
                groups[group_name] = []

            groups[group_name].append(team_name)

    return groups


def validate_groups_have_ratings(groups, teams):
    missing_teams = []

    for group_name, group_teams in groups.items():
        for team in group_teams:
            if team not in teams:
                missing_teams.append(team)

    if missing_teams:
        raise ValueError(f"Missing ratings for these teams: {missing_teams}")


teams = load_teams("data/teams.csv")
groups = load_groups("data/groups.csv")

validate_groups_have_ratings(groups, teams)