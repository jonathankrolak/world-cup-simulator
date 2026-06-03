# 2026 World Cup Simulator

A Python + Streamlit app that simulates the 2026 FIFA World Cup using team ratings, group-stage rules, knockout rounds, penalty shootouts, and Monte Carlo simulations.

## Live App

https://world-cup-simulator-4foucz3rugtwevtqvfb8xd.streamlit.app/

## Features

- Simulates the 2026 World Cup format
- Uses FIFA ranking-point-based team strength
- Runs Monte Carlo simulations
- Shows each team's odds of reaching each stage:
  - Knockout stage
  - Round of 16
  - Quarterfinals
  - Semifinals
  - Final
  - Champion
- Includes penalty shootouts
- Interactive Streamlit dashboard
- Team dropdown for individual team odds

## Tech Stack

- Python
- Streamlit
- Pandas
- CSV data
- Monte Carlo simulation

## Run Locally

Install dependencies:

```bash
python -m pip install -r requirements.txt

Run the app:

python -m streamlit run app.py
Project Structure
world-cup-simulator/
├── app.py
├── simulator.py
├── tournament.py
├── group_stage.py
├── knockout_stage.py
├── match.py
├── data.py
├── requirements.txt
└── data/
    ├── teams.csv
    └── groups.csv
Note

This is a simulation project for learning and portfolio purposes. It is not an official FIFA prediction model.