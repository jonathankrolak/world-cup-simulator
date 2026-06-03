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

    st.subheader("Simulation Results")
    st.dataframe(display_df, use_container_width=True)

    st.subheader("Top Champion Odds")

    top_champion_odds = results_df.head(10).set_index("team")["champion_percentage"]

    st.bar_chart(top_champion_odds)

else:
    st.info("Choose the number of simulations, then click **Run simulations**.")