# NFL WAR Lab

A repository-ready Streamlit dashboard for Matchup Intelligence LLC. The site presents 2022–2025 NFL WAR outputs through public-facing tabs for team value, non-QB roster strength, draft-class surplus, draft-capital efficiency, non-QB drafting, and player-level exploration.

## Included tabs

1. **Overview** — dashboard guide and top-level snapshots.
2. **Team WAR + Value** — team-season WAR, wins, playoffs, surplus value, and WAR efficiency.
3. **Team Non-QB WAR** — accumulated supporting-roster WAR after removing quarterbacks.
4. **Draft Surplus** — leading draft classes by rookie-contract cap surplus.
5. **Draft Efficiency** — total-WAR draft-class efficiency relative to Fitzgerald–Spielberger capital.
6. **Non-QB Drafting** — accumulated non-QB WAR and opportunity-adjusted non-QB capital efficiency.
7. **Player Explorer** — filterable player-season WAR table.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy through Streamlit Community Cloud

1. Create a GitHub repository.
2. Add the contents of this folder to the repository root.
3. In Streamlit Community Cloud, select **Create app**.
4. Choose the repository, branch, and `app.py` as the main file.
5. Deploy.

The `data/` folder must remain in the repository because the app reads the CSV files with relative paths.

## Data files

- `draft_class_non_qb_war_accumulated_2022_2025.csv`
- `draft_class_non_qb_war_efficiency_2022_2025.csv`
- `team_non_qb_war_leaderboard_2022_2025.csv`
- `top15_draft_classes_by_draft_efficiency.csv`
- `top15_draft_classes_by_cap_surplus.csv`
- `player_season_war_2022_2025.csv`
- `team_war_cap_value_2022_2025_formatted.csv`

## Branding

The landing-page title, accent colors, and footer language can be edited directly in `app.py`. The visual system is intentionally independent rather than copying another publication's proprietary branding.
