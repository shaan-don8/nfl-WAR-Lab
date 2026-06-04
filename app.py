from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NFL WAR Lab | Matchup Intelligence",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

TEAM_CODE_MAP = {
    "ARZ": "ARI",
    "BLT": "BAL",
    "CLV": "CLE",
    "HST": "HOU",
    "GNB": "GB",
    "KAN": "KC",
    "LAR": "LA",
    "LVR": "LV",
    "NOR": "NO",
    "NWE": "NE",
    "SFO": "SF",
    "TAM": "TB",
}

TEAM_NAMES = {
    "ARI": "Arizona Cardinals",
    "ATL": "Atlanta Falcons",
    "BAL": "Baltimore Ravens",
    "BUF": "Buffalo Bills",
    "CAR": "Carolina Panthers",
    "CHI": "Chicago Bears",
    "CIN": "Cincinnati Bengals",
    "CLE": "Cleveland Browns",
    "DAL": "Dallas Cowboys",
    "DEN": "Denver Broncos",
    "DET": "Detroit Lions",
    "GB": "Green Bay Packers",
    "HOU": "Houston Texans",
    "IND": "Indianapolis Colts",
    "JAX": "Jacksonville Jaguars",
    "KC": "Kansas City Chiefs",
    "LA": "Los Angeles Rams",
    "LAC": "Los Angeles Chargers",
    "LV": "Las Vegas Raiders",
    "MIA": "Miami Dolphins",
    "MIN": "Minnesota Vikings",
    "NE": "New England Patriots",
    "NO": "New Orleans Saints",
    "NYG": "New York Giants",
    "NYJ": "New York Jets",
    "PHI": "Philadelphia Eagles",
    "PIT": "Pittsburgh Steelers",
    "SEA": "Seattle Seahawks",
    "SF": "San Francisco 49ers",
    "TB": "Tampa Bay Buccaneers",
    "TEN": "Tennessee Titans",
    "WAS": "Washington Commanders",
}

# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>
        :root {
            --page-bg: #07111F;
            --panel-bg: #0D1B2A;
            --panel-bg-2: #11263B;
            --line: rgba(255,255,255,0.10);
            --text: #F4F7FB;
            --muted: #A8B5C5;
            --accent: #F6B73C;
            --accent-2: #4EC9B0;
            --accent-3: #FF6B6B;
        }

        .stApp {
            background: linear-gradient(160deg, #07111F 0%, #0A1727 48%, #081321 100%);
            color: var(--text);
        }

        [data-testid="stSidebar"] {
            background: #07111F;
            border-right: 1px solid var(--line);
        }

        [data-testid="stHeader"] {
            background: rgba(7,17,31,0.86);
        }

        .block-container {
            max-width: 1550px;
            padding-top: 1.4rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3, h4 {
            letter-spacing: -0.025em;
        }

        .brand-kicker {
            color: var(--accent);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.19em;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }

        .brand-title {
            color: var(--text);
            font-size: clamp(2rem, 4vw, 4rem);
            line-height: 0.96;
            font-weight: 900;
            margin: 0;
        }

        .brand-subtitle {
            color: var(--muted);
            max-width: 920px;
            font-size: 1.03rem;
            line-height: 1.6;
            margin-top: 0.8rem;
        }

        .section-kicker {
            color: var(--accent);
            text-transform: uppercase;
            font-size: 0.72rem;
            letter-spacing: 0.15em;
            font-weight: 800;
            margin-bottom: 0.25rem;
        }

        .section-title {
            color: var(--text);
            font-size: 1.75rem;
            font-weight: 850;
            line-height: 1.1;
            margin: 0;
        }

        .section-copy {
            color: var(--muted);
            font-size: 0.96rem;
            line-height: 1.55;
            max-width: 1000px;
            margin-top: 0.45rem;
            margin-bottom: 0.9rem;
        }

        .metric-card {
            background: linear-gradient(145deg, rgba(17,38,59,0.94), rgba(13,27,42,0.96));
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 1rem 1.1rem;
            min-height: 112px;
            box-shadow: 0 12px 28px rgba(0,0,0,0.12);
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.73rem;
            font-weight: 800;
            letter-spacing: 0.11em;
            text-transform: uppercase;
        }

        .metric-value {
            color: var(--text);
            font-size: 1.82rem;
            font-weight: 900;
            letter-spacing: -0.045em;
            line-height: 1.08;
            margin-top: 0.34rem;
        }

        .metric-note {
            color: var(--muted);
            font-size: 0.78rem;
            line-height: 1.35;
            margin-top: 0.38rem;
        }

        .feature-card {
            background: rgba(13,27,42,0.84);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 1rem 1.1rem;
            min-height: 160px;
        }

        .feature-number {
            color: var(--accent);
            font-weight: 900;
            font-size: 1.4rem;
        }

        .feature-title {
            color: var(--text);
            font-weight: 850;
            font-size: 1rem;
            margin-top: 0.2rem;
        }

        .feature-copy, .data-note {
            color: var(--muted);
            font-size: 0.88rem;
            line-height: 1.5;
            margin-top: 0.45rem;
        }

        .callout {
            background: rgba(246,183,60,0.08);
            border-left: 3px solid var(--accent);
            border-radius: 8px;
            padding: 0.85rem 1rem;
            color: #E4ECF4;
            font-size: 0.92rem;
            line-height: 1.5;
            margin: 0.9rem 0 1rem 0;
        }

        .sidebar-brand {
            font-size: 1.15rem;
            font-weight: 900;
            color: #F4F7FB;
            line-height: 1.05;
            margin-bottom: 0.3rem;
        }

        .sidebar-copy {
            color: #A8B5C5;
            font-size: 0.82rem;
            line-height: 1.45;
        }

        .footer-note {
            border-top: 1px solid var(--line);
            color: var(--muted);
            font-size: 0.78rem;
            line-height: 1.5;
            margin-top: 2rem;
            padding-top: 1rem;
        }

        button[data-baseweb="tab"] {
            background: transparent;
            border-radius: 10px 10px 0 0;
            color: #C9D4DF;
            font-weight: 750;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            background: rgba(246,183,60,0.08);
            color: #F6B73C;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 10px;
            overflow: hidden;
        }

        .stDownloadButton button {
            border: 1px solid rgba(246,183,60,0.55);
            background: rgba(246,183,60,0.09);
            color: #F5D28B;
            border-radius: 9px;
            font-weight: 800;
        }

        div[data-testid="stMetric"] {
            background: rgba(13,27,42,0.76);
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 0.7rem 0.85rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DATA HELPERS
# ============================================================


def canonicalize_team(series: pd.Series) -> pd.Series:
    return series.replace(TEAM_CODE_MAP)


def parse_money(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str).str.replace(r"[$,]", "", regex=True),
        errors="coerce",
    )


def clean_percentage(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series.astype(str).str.replace("%", "", regex=False), errors="coerce")


def clean_multiple(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series.astype(str).str.replace("x", "", regex=False), errors="coerce")


@st.cache_data(show_spinner=False)
def load_data() -> dict[str, pd.DataFrame]:
    data = {
        "draft_non_qb_accum": pd.read_csv(DATA_DIR / "draft_class_non_qb_war_accumulated_2022_2025.csv"),
        "draft_non_qb_eff": pd.read_csv(DATA_DIR / "draft_class_non_qb_war_efficiency_2022_2025.csv"),
        "team_non_qb": pd.read_csv(DATA_DIR / "team_non_qb_war_leaderboard_2022_2025.csv"),
        "draft_eff": pd.read_csv(DATA_DIR / "top15_draft_classes_by_draft_efficiency.csv"),
        "draft_surplus": pd.read_csv(DATA_DIR / "top15_draft_classes_by_cap_surplus.csv"),
        "players": pd.read_csv(DATA_DIR / "player_season_war_2022_2025.csv"),
        "team_value": pd.read_csv(DATA_DIR / "team_war_cap_value_2022_2025_formatted.csv"),
    }

    for key in ["draft_non_qb_accum", "draft_non_qb_eff", "draft_eff", "draft_surplus"]:
        data[key]["draft_team"] = canonicalize_team(data[key]["draft_team"])

    data["team_non_qb"]["team"] = canonicalize_team(data["team_non_qb"]["team"])
    data["players"]["team"] = canonicalize_team(data["players"]["team"])
    data["team_value"]["team"] = canonicalize_team(data["team_value"]["team"])

    data["team_value"]["team_surplus_dollars_numeric"] = parse_money(data["team_value"]["team_surplus_dollars"])
    data["team_value"]["team_war_value_dollars_numeric"] = parse_money(data["team_value"]["team_war_value_dollars"])
    data["team_value"]["salary_cap_numeric"] = parse_money(data["team_value"]["salary_cap"])
    data["team_value"]["team_cap_value_multiple_numeric"] = clean_multiple(data["team_value"]["team_cap_value_multiple"])
    data["team_value"]["team_surplus_pct_of_cap_numeric"] = clean_percentage(data["team_value"]["team_surplus_pct_of_cap"])

    data["players"]["position"] = data["players"]["position"].fillna("Unclassified")
    data["players"]["unit"] = data["players"]["unit"].fillna("Unclassified")

    return data


def add_team_name(df: pd.DataFrame, team_col: str = "team") -> pd.DataFrame:
    out = df.copy()
    out["team_name"] = out[team_col].map(TEAM_NAMES).fillna(out[team_col])
    return out


def metric_card(label: str, value: str, note: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(kicker: str, title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="section-kicker">{kicker}</div>
        <div class="section-title">{title}</div>
        <div class="section-copy">{copy}</div>
        """,
        unsafe_allow_html=True,
    )


def csv_download(df: pd.DataFrame, filename: str, label: str = "Download filtered CSV") -> None:
    st.download_button(
        label=label,
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=filename,
        mime="text/csv",
        use_container_width=False,
    )


def horizontal_bar(
    df: pd.DataFrame,
    *,
    value_col: str,
    label_col: str,
    title: str,
    hover_cols: Iterable[str] | None = None,
    value_label: str | None = None,
) -> None:
    chart_df = df.sort_values(value_col, ascending=True).copy()
    fig = px.bar(
        chart_df,
        x=value_col,
        y=label_col,
        orientation="h",
        hover_data=list(hover_cols or []),
        title=title,
    )
    fig.update_traces(marker_color="#F6B73C")
    fig.update_layout(
        height=max(440, 31 * len(chart_df)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#D9E3ED",
        title_font_color="#F4F7FB",
        margin=dict(l=10, r=10, t=60, b=10),
        xaxis_title=value_label or value_col.replace("_", " ").title(),
        yaxis_title="",
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.22)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.02)"),
    )
    st.plotly_chart(fig, use_container_width=True)


def apply_team_filter(df: pd.DataFrame, column: str, label: str, key: str) -> pd.DataFrame:
    team_options = sorted(df[column].dropna().astype(str).unique())
    selected = st.multiselect(label, team_options, default=[], key=key)
    if selected:
        return df[df[column].isin(selected)].copy()
    return df.copy()


DATA = load_data()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown('<div class="sidebar-brand">NFL WAR Lab</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-copy">A Matchup Intelligence leaderboard hub for NFL player value, roster construction, surplus value, and draft efficiency.</div>',
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown("**Coverage window**")
    st.caption("2022–2025 regular-season WAR outputs")
    st.markdown("**Model lens**")
    st.caption("EPA-based WAR with roster-value and draft-capital extensions")
    st.markdown("**Navigation**")
    st.caption("Use the horizontal tabs at the top of the page. Each table is sortable, filterable, and downloadable.")
    st.divider()
    st.caption("Built by Matchup Intelligence LLC")

# ============================================================
# HEADER
# ============================================================

st.markdown('<div class="brand-kicker">Matchup Intelligence LLC</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-title">NFL WAR Lab</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="brand-subtitle">
        Explore how NFL teams create value across the roster. Toggle between team WAR, cap efficiency,
        non-quarterback roster strength, draft-class surplus, draft-capital efficiency, and player-level WAR outputs.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

(
    tab_home,
    tab_team_value,
    tab_team_non_qb,
    tab_draft_surplus,
    tab_draft_eff,
    tab_non_qb_draft,
    tab_players,
) = st.tabs(
    [
        "Overview",
        "Team WAR + Value",
        "Team Non-QB WAR",
        "Draft Surplus",
        "Draft Efficiency",
        "Non-QB Drafting",
        "Player Explorer",
    ]
)

# ============================================================
# OVERVIEW TAB
# ============================================================

with tab_home:
    players = DATA["players"]
    team_non_qb = DATA["team_non_qb"]
    team_value = DATA["team_value"]
    draft_non_qb_eff = DATA["draft_non_qb_eff"]

    section_header(
        "Dashboard guide",
        "A roster-construction lens for NFL WAR",
        "The site separates raw production from cost efficiency. Use the team tabs to evaluate roster strength, the draft tabs to evaluate talent acquisition, and the player explorer to inspect the underlying WAR outputs.",
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Player-season rows", f"{len(players):,}", "Underlying player WAR observations")
    with c2:
        metric_card("NFL teams", f"{team_non_qb['team'].nunique():,}", "Canonical team abbreviations")
    with c3:
        metric_card("Seasons", f"{players['season'].nunique():,}", "2022 through 2025")
    with c4:
        metric_card("Total WAR", f"{players['total_war'].sum():.1f}", "Across all player-season rows")

    st.write("")
    st.markdown(
        """
        <div class="callout">
            <strong>How to read the dashboard:</strong> raw WAR identifies production. Surplus value compares WAR output with cap cost.
            Draft-efficiency metrics compare output with the Fitzgerald–Spielberger value of the selections invested. The non-QB tabs remove quarterback WAR to isolate supporting-roster construction.
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    features = [
        ("01", "Team WAR + Value", "Compare wins, total WAR, offensive WAR, defensive WAR, estimated surplus value, and WAR efficiency by team-season."),
        ("02", "Non-QB roster strength", "Identify the teams that accumulated the strongest supporting-roster WAR totals after removing quarterback value."),
        ("03", "Draft-class economics", "Separate raw draft production from surplus value and draft-capital efficiency. Premium picks carry a larger acquisition-cost denominator."),
    ]
    for col, (number, title, copy) in zip([c1, c2, c3], features):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-number">{number}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-copy">{copy}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    section_header(
        "Snapshot",
        "Leading non-QB roster builders",
        "Philadelphia leads the 2022–2025 team-level non-QB WAR table. The draft-capital leaderboard provides a second view: how efficiently did recent classes generate supporting-roster value relative to the capital invested?",
    )
    left, right = st.columns(2)
    with left:
        top = add_team_name(team_non_qb.head(10), "team")
        horizontal_bar(
            top,
            value_col="non_qb_war",
            label_col="team_name",
            title="Top teams by accumulated non-QB WAR, 2022–2025",
            hover_cols=["avg_non_qb_war_per_season"],
            value_label="Accumulated non-QB WAR",
        )
    with right:
        top_eff = draft_non_qb_eff.head(10).copy()
        top_eff["class"] = top_eff["draft_year"].astype(str) + " " + top_eff["draft_team"]
        horizontal_bar(
            top_eff,
            value_col="opportunity_adjusted_efficiency_index",
            label_col="class",
            title="Top non-QB draft classes by opportunity-adjusted efficiency",
            hover_cols=["non_qb_war", "non_qb_fs_points", "seasons_possible"],
            value_label="Opportunity-adjusted efficiency index",
        )

# ============================================================
# TEAM WAR + VALUE TAB
# ============================================================

with tab_team_value:
    section_header(
        "Team economics",
        "Team WAR and cap-value efficiency",
        "Compare each team-season using total WAR, offense, defense, wins, estimated surplus value, and the WAR efficiency index. The efficiency index uses 100 as the league-average benchmark for value produced relative to the cap.",
    )

    df = DATA["team_value"].copy()
    f1, f2, f3 = st.columns([1, 1, 1.5])
    with f1:
        seasons = sorted(df["season"].unique())
        selected_seasons = st.multiselect("Season", seasons, default=seasons, key="team_value_seasons")
    with f2:
        playoff_filter = st.selectbox("Playoff filter", ["All teams", "Playoff teams", "Non-playoff teams"], key="team_value_playoff")
    with f3:
        selected_teams = st.multiselect("Team", sorted(df["team"].unique()), default=[], key="team_value_teams")

    if selected_seasons:
        df = df[df["season"].isin(selected_seasons)]
    if playoff_filter == "Playoff teams":
        df = df[df["made_playoffs"].eq("Y")]
    elif playoff_filter == "Non-playoff teams":
        df = df[~df["made_playoffs"].eq("Y")]
    if selected_teams:
        df = df[df["team"].isin(selected_teams)]

    metric_options = {
        "WAR efficiency index": "war_efficiency_index",
        "Total WAR": "total_war",
        "Offensive WAR": "offensive_war",
        "Defensive WAR": "defensive_war",
        "Wins": "wins",
        "Surplus value ($)": "team_surplus_dollars_numeric",
    }
    selected_metric_label = st.selectbox("Chart metric", list(metric_options), index=0, key="team_value_metric")
    selected_metric = metric_options[selected_metric_label]

    chart_df = df.dropna(subset=[selected_metric]).copy()
    chart_df["label"] = chart_df["season"].astype(str) + " " + chart_df["team"]
    horizontal_bar(
        chart_df.sort_values(selected_metric, ascending=False).head(20),
        value_col=selected_metric,
        label_col="label",
        title=f"Top 20 team-seasons by {selected_metric_label.lower()}",
        hover_cols=["wins", "losses", "total_war", "offensive_war", "defensive_war", "made_playoffs"],
        value_label=selected_metric_label,
    )

    table = df[
        [
            "season", "team", "record", "made_playoffs", "postseason_round_reached", "total_war",
            "offensive_war", "defensive_war", "team_war_value_dollars", "team_surplus_dollars",
            "team_cap_value_multiple", "war_efficiency_index",
        ]
    ].sort_values(["season", "war_efficiency_index"], ascending=[False, False])

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "total_war": st.column_config.NumberColumn("Total WAR", format="%.2f"),
            "offensive_war": st.column_config.NumberColumn("Offensive WAR", format="%.2f"),
            "defensive_war": st.column_config.NumberColumn("Defensive WAR", format="%.2f"),
            "war_efficiency_index": st.column_config.NumberColumn("WAR Efficiency Index", format="%.1f"),
        },
    )
    csv_download(table, "filtered_team_war_cap_value.csv")

# ============================================================
# TEAM NON-QB TAB
# ============================================================

with tab_team_non_qb:
    section_header(
        "Supporting roster",
        "Team non-QB WAR leaderboard",
        "This table removes quarterback WAR and sums the remaining player value by team from 2022–2025. It is designed to identify the strongest supporting rosters rather than teams driven primarily by quarterback production.",
    )

    df = add_team_name(DATA["team_non_qb"], "team")
    top_n = st.slider("Teams shown in chart", min_value=5, max_value=32, value=15, key="team_non_qb_topn")
    horizontal_bar(
        df.head(top_n),
        value_col="non_qb_war",
        label_col="team_name",
        title="Accumulated non-QB WAR by team, 2022–2025",
        hover_cols=["avg_non_qb_war_per_season", "unique_non_qb_players"],
        value_label="Accumulated non-QB WAR",
    )

    table = df[
        ["rank", "team", "team_name", "non_qb_war", "avg_non_qb_war_per_season", "non_qb_player_seasons", "unique_non_qb_players"]
    ]
    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "non_qb_war": st.column_config.NumberColumn("Non-QB WAR", format="%.3f"),
            "avg_non_qb_war_per_season": st.column_config.NumberColumn("Avg. non-QB WAR / season", format="%.3f"),
        },
    )
    csv_download(table, "team_non_qb_war_leaderboard_2022_2025.csv")

# ============================================================
# DRAFT SURPLUS TAB
# ============================================================

with tab_draft_surplus:
    section_header(
        "Rookie-contract value",
        "Draft classes by cap surplus",
        "This leaderboard estimates the gap between each draft class's WAR market value and its cap hits. It captures how much excess value teams generated while players remained on cost-controlled contracts.",
    )

    df = DATA["draft_surplus"].copy()
    df["class"] = df["draft_year"].astype(str) + " " + df["draft_team"]
    horizontal_bar(
        df,
        value_col="surplus_per_season_m",
        label_col="class",
        title="Top draft classes by cap surplus per season",
        hover_cols=["total_war", "war_market_value_m", "cap_hit_m", "surplus_m", "seasons_elapsed"],
        value_label="Cap surplus per season ($M)",
    )

    table = df[
        ["rank", "draft_year", "draft_team", "total_war", "war_market_value_m", "cap_hit_m", "surplus_m", "seasons_elapsed", "surplus_per_season_m"]
    ]
    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "total_war": st.column_config.NumberColumn("Total WAR", format="%.2f"),
            "war_market_value_m": st.column_config.NumberColumn("WAR market value ($M)", format="%.2f"),
            "cap_hit_m": st.column_config.NumberColumn("Cap hit ($M)", format="%.2f"),
            "surplus_m": st.column_config.NumberColumn("Surplus ($M)", format="%.2f"),
            "surplus_per_season_m": st.column_config.NumberColumn("Surplus / season ($M)", format="%.2f"),
        },
    )
    csv_download(table, "top15_draft_classes_by_cap_surplus.csv")

# ============================================================
# DRAFT EFFICIENCY TAB
# ============================================================

with tab_draft_eff:
    section_header(
        "Draft capital",
        "Draft classes by total-WAR capital efficiency",
        "This leaderboard compares total WAR value with the Fitzgerald–Spielberger points invested in each draft class. A premium pick carries a larger acquisition-cost denominator than a late-round selection.",
    )

    df = DATA["draft_eff"].copy()
    df["class"] = df["draft_year"].astype(str) + " " + df["draft_team"]
    horizontal_bar(
        df,
        value_col="draft_efficiency_index",
        label_col="class",
        title="Top draft classes by total-WAR draft efficiency index",
        hover_cols=["total_war", "draft_capital_points", "surplus_m", "war_value_per_1000_fs_points"],
        value_label="Draft efficiency index",
    )

    table = df[
        [
            "rank", "draft_year", "draft_team", "total_war", "war_market_value_m", "surplus_m",
            "draft_capital_points", "war_value_per_1000_fs_points", "surplus_per_1000_fs_points", "draft_efficiency_index",
        ]
    ]
    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "total_war": st.column_config.NumberColumn("Total WAR", format="%.2f"),
            "war_market_value_m": st.column_config.NumberColumn("WAR market value ($M)", format="%.2f"),
            "surplus_m": st.column_config.NumberColumn("Surplus ($M)", format="%.2f"),
            "draft_capital_points": st.column_config.NumberColumn("FS points", format="%.0f"),
            "war_value_per_1000_fs_points": st.column_config.NumberColumn("WAR value / 1,000 FS ($M)", format="%.2f"),
            "surplus_per_1000_fs_points": st.column_config.NumberColumn("Surplus / 1,000 FS ($M)", format="%.2f"),
            "draft_efficiency_index": st.column_config.NumberColumn("Draft efficiency index", format="%.1f"),
        },
    )
    csv_download(table, "top15_draft_classes_by_draft_efficiency.csv")

# ============================================================
# NON-QB DRAFTING TAB
# ============================================================

with tab_non_qb_draft:
    section_header(
        "Supporting-roster acquisition",
        "Non-QB draft-class leaderboards",
        "Toggle between accumulated supporting-roster production and capital-adjusted efficiency. The efficiency view prevents teams from receiving the same credit for a premium-pick hit as for a late-round breakout.",
    )

    sub_accum, sub_eff = st.tabs(["Accumulated non-QB WAR", "Capital-adjusted non-QB efficiency"])

    with sub_accum:
        df = DATA["draft_non_qb_accum"].copy()
        f1, f2 = st.columns([1, 2])
        with f1:
            years = sorted(df["draft_year"].unique())
            selected_years = st.multiselect("Draft year", years, default=years, key="nqb_accum_years")
        with f2:
            selected_teams = st.multiselect("Drafting team", sorted(df["draft_team"].unique()), default=[], key="nqb_accum_teams")
        if selected_years:
            df = df[df["draft_year"].isin(selected_years)]
        if selected_teams:
            df = df[df["draft_team"].isin(selected_teams)]

        chart_df = df.sort_values("non_qb_war", ascending=False).head(25).copy()
        chart_df["class"] = chart_df["draft_year"].astype(str) + " " + chart_df["draft_team"]
        horizontal_bar(
            chart_df,
            value_col="non_qb_war",
            label_col="class",
            title="Top draft classes by accumulated non-QB WAR",
            hover_cols=["players_with_war_rows", "seasons_possible", "non_qb_war_per_possible_season"],
            value_label="Accumulated non-QB WAR",
        )

        table = df.sort_values("non_qb_war", ascending=False).reset_index(drop=True).copy()
        table["rank_filtered"] = table.index + 1
        table = table[
            [
                "rank_filtered", "draft_year", "draft_team", "non_qb_war", "players_with_war_rows",
                "player_season_rows", "seasons_possible", "non_qb_war_per_possible_season", "non_qb_war_per_player",
            ]
        ]
        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "rank_filtered": "Rank",
                "non_qb_war": st.column_config.NumberColumn("Non-QB WAR", format="%.3f"),
                "non_qb_war_per_possible_season": st.column_config.NumberColumn("Non-QB WAR / possible season", format="%.3f"),
                "non_qb_war_per_player": st.column_config.NumberColumn("Non-QB WAR / player with row", format="%.3f"),
            },
        )
        csv_download(table, "filtered_draft_class_non_qb_war_accumulated.csv")

    with sub_eff:
        df = DATA["draft_non_qb_eff"].copy()
        f1, f2, f3 = st.columns([1, 1, 2])
        with f1:
            years = sorted(df["draft_year"].unique())
            selected_years = st.multiselect("Draft year", years, default=years, key="nqb_eff_years")
        with f2:
            min_picks = st.slider("Minimum non-QB picks", min_value=1, max_value=int(df["total_non_qb_picks"].max()), value=1, key="nqb_eff_min_picks")
        with f3:
            selected_teams = st.multiselect("Drafting team", sorted(df["draft_team"].unique()), default=[], key="nqb_eff_teams")
        if selected_years:
            df = df[df["draft_year"].isin(selected_years)]
        df = df[df["total_non_qb_picks"] >= min_picks]
        if selected_teams:
            df = df[df["draft_team"].isin(selected_teams)]

        metric_options = {
            "Opportunity-adjusted efficiency index": "opportunity_adjusted_efficiency_index",
            "Realized draft efficiency index": "non_qb_draft_efficiency_index",
            "Non-QB WAR per 1,000 FS points": "non_qb_war_per_1000_fs",
            "Non-QB WAR per 1,000 FS-point seasons": "non_qb_war_per_1000_fs_seasons",
        }
        metric_label = st.selectbox("Efficiency lens", list(metric_options), key="nqb_eff_metric")
        metric = metric_options[metric_label]

        chart_df = df.sort_values(metric, ascending=False).head(25).copy()
        chart_df["class"] = chart_df["draft_year"].astype(str) + " " + chart_df["draft_team"]
        horizontal_bar(
            chart_df,
            value_col=metric,
            label_col="class",
            title=f"Top non-QB draft classes by {metric_label.lower()}",
            hover_cols=["non_qb_war", "non_qb_fs_points", "seasons_possible", "total_non_qb_picks"],
            value_label=metric_label,
        )

        table = df.sort_values(metric, ascending=False).reset_index(drop=True).copy()
        table["rank_filtered"] = table.index + 1
        table = table[
            [
                "rank_filtered", "draft_year", "draft_team", "non_qb_war", "non_qb_fs_points", "seasons_possible",
                "non_qb_war_per_1000_fs", "non_qb_draft_efficiency_index", "non_qb_war_per_1000_fs_seasons",
                "opportunity_adjusted_efficiency_index", "total_non_qb_picks", "players_with_war_rows",
            ]
        ]
        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "rank_filtered": "Rank",
                "non_qb_war": st.column_config.NumberColumn("Non-QB WAR", format="%.3f"),
                "non_qb_war_per_1000_fs": st.column_config.NumberColumn("Non-QB WAR / 1,000 FS", format="%.3f"),
                "non_qb_draft_efficiency_index": st.column_config.NumberColumn("Realized efficiency index", format="%.1f"),
                "non_qb_war_per_1000_fs_seasons": st.column_config.NumberColumn("Non-QB WAR / 1,000 FS-point seasons", format="%.3f"),
                "opportunity_adjusted_efficiency_index": st.column_config.NumberColumn("Opportunity-adjusted index", format="%.1f"),
            },
        )
        csv_download(table, "filtered_draft_class_non_qb_war_efficiency.csv")

# ============================================================
# PLAYER EXPLORER TAB
# ============================================================

with tab_players:
    section_header(
        "Underlying outputs",
        "Player-season WAR explorer",
        "Filter and inspect the player-season table underlying the team-level leaderboards. Use the unit and position filters to isolate quarterbacks, skill players, offensive linemen, or defenders.",
    )

    df = DATA["players"].copy()
    f1, f2, f3, f4 = st.columns([1, 1.4, 1.4, 1.8])
    with f1:
        seasons = sorted(df["season"].unique())
        selected_seasons = st.multiselect("Season", seasons, default=seasons, key="player_seasons")
    with f2:
        selected_teams = st.multiselect("Team", sorted(df["team"].unique()), default=[], key="player_teams")
    with f3:
        selected_units = st.multiselect("Unit", sorted(df["unit"].unique()), default=[], key="player_units")
    with f4:
        search = st.text_input("Player search", placeholder="Type a player name", key="player_search")

    f5, f6 = st.columns([2, 1])
    with f5:
        selected_positions = st.multiselect("Position", sorted(df["position"].unique()), default=[], key="player_positions")
    with f6:
        rows_shown = st.slider("Rows shown", min_value=25, max_value=300, value=100, step=25, key="player_rows")

    if selected_seasons:
        df = df[df["season"].isin(selected_seasons)]
    if selected_teams:
        df = df[df["team"].isin(selected_teams)]
    if selected_units:
        df = df[df["unit"].isin(selected_units)]
    if selected_positions:
        df = df[df["position"].isin(selected_positions)]
    if search.strip():
        df = df[df["player_name"].str.contains(search.strip(), case=False, na=False)]

    df = df.sort_values("total_war", ascending=False)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Filtered rows", f"{len(df):,}")
    with c2:
        st.metric("Filtered total WAR", f"{df['total_war'].sum():.2f}")
    with c3:
        st.metric("Unique players", f"{df['player_group_key'].nunique():,}")

    table = df[
        [
            "season", "team", "player_name", "position", "unit", "total_war", "offensive_war", "defensive_war",
            "offensive_epa", "defensive_epa", "offensive_volume", "defensive_snaps",
        ]
    ].head(rows_shown)

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "total_war": st.column_config.NumberColumn("Total WAR", format="%.3f"),
            "offensive_war": st.column_config.NumberColumn("Offensive WAR", format="%.3f"),
            "defensive_war": st.column_config.NumberColumn("Defensive WAR", format="%.3f"),
            "offensive_epa": st.column_config.NumberColumn("Offensive EPA", format="%.2f"),
            "defensive_epa": st.column_config.NumberColumn("Defensive EPA", format="%.2f"),
            "offensive_volume": st.column_config.NumberColumn("Offensive volume", format="%.0f"),
            "defensive_snaps": st.column_config.NumberColumn("Defensive snaps", format="%.0f"),
        },
    )
    csv_download(df, "filtered_player_season_war_2022_2025.csv")

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-note">
        <strong>Methodology note:</strong> This dashboard presents 2022–2025 WAR outputs and derived roster-economics tables supplied by Matchup Intelligence LLC.
        Non-QB tables remove rows tagged as quarterback. Draft-capital tables use Fitzgerald–Spielberger points to account for the acquisition cost associated with each selection.
        Tables can be sorted interactively and downloaded as CSV files.
    </div>
    """,
    unsafe_allow_html=True,
)
