import pandas as pd
import streamlit as st

from simulator import run_simulations


st.set_page_config(
    page_title="2026 World Cup Simulator",
    page_icon="⚽",
    layout="wide",
)


st.title("2026 World Cup Simulator")
st.write(
    "Run Monte Carlo simulations of the 2026 World Cup using FIFA ranking-point-based team strength."
)

number_of_simulations = st.slider(
    "Number of simulations",
    min_value=100,
    max_value=50000,
    value=10000,
    step=100,
)

run_button = st.button("Run simulations")

if run_button:
    with st.spinner(f"Running {number_of_simulations:,} simulations..."):
        results = run_simulations(number_of_simulations)

    results_df = pd.DataFrame(results)

    st.session_state["results_df"] = results_df
    st.session_state["number_of_simulations"] = number_of_simulations


if "results_df" not in st.session_state:
    st.info("Choose the number of simulations, then click **Run simulations**.")
else:
    results_df = st.session_state["results_df"]
    number_of_simulations = st.session_state["number_of_simulations"]

    st.subheader(f"Simulation Results: {number_of_simulations:,} Runs")

    team_options = results_df["team"].sort_values().tolist()

    selected_team = st.selectbox(
        "Select a team to highlight",
        team_options,
        index=team_options.index("USA") if "USA" in team_options else 0,
    )

    selected_team_row = results_df[results_df["team"] == selected_team].iloc[0]

    best_champion_team = results_df.iloc[0]
    best_final_team = results_df.sort_values(
        by="final_percentage",
        ascending=False,
    ).iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label=f"{selected_team} Champion Odds",
            value=f"{selected_team_row['champion_percentage']:.2f}%",
        )

    with col2:
        st.metric(
            label=f"{selected_team} Final Odds",
            value=f"{selected_team_row['final_percentage']:.2f}%",
        )

    with col3:
        st.metric(
            label=f"{selected_team} Advance Odds",
            value=f"{selected_team_row['advance_percentage']:.2f}%",
        )

    st.write(
        f"**Most likely champion:** {best_champion_team['team']} "
        f"({best_champion_team['champion_percentage']:.2f}%)"
    )

    st.write(
        f"**Most likely to reach the final:** {best_final_team['team']} "
        f"({best_final_team['final_percentage']:.2f}%)"
    )

    st.subheader(f"{selected_team} Tournament Path Odds")

    selected_team_path = pd.DataFrame(
        {
            "Stage": [
                "Advance",
                "Round of 16",
                "Quarterfinal",
                "Semifinal",
                "Final",
                "Champion",
            ],
            "Percentage": [
                selected_team_row["advance_percentage"],
                selected_team_row["round_of_16_percentage"],
                selected_team_row["quarterfinal_percentage"],
                selected_team_row["semifinal_percentage"],
                selected_team_row["final_percentage"],
                selected_team_row["champion_percentage"],
            ],
        }
    )

    st.bar_chart(
        selected_team_path,
        x="Stage",
        y="Percentage",
    )

    display_df = results_df.rename(
        columns={
            "team": "Team",
            "advance_percentage": "Advance %",
            "round_of_16_percentage": "Round of 16 %",
            "quarterfinal_percentage": "Quarterfinal %",
            "semifinal_percentage": "Semifinal %",
            "final_percentage": "Final %",
            "champion_percentage": "Champion %",
            "championships_won": "Titles Won",
        }
    )

    percentage_columns = [
        "Advance %",
        "Round of 16 %",
        "Quarterfinal %",
        "Semifinal %",
        "Final %",
        "Champion %",
    ]

    for column in percentage_columns:
        display_df[column] = display_df[column].map(lambda value: f"{value:.2f}%")

    st.subheader("Full Team Odds Table")
    st.dataframe(display_df, use_container_width=True)

    st.subheader("Top 10 Champion Odds")

    top_champion_odds = results_df.head(10).set_index("team")["champion_percentage"]

    st.bar_chart(top_champion_odds)