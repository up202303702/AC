"""Plain-language names for columns, and a footnote helper, so every plot can be read on its own."""

LABELS = {
    # teams
    "last_pts_vs_avg": "points last season",
    "avg3_pts_vs_avg": "points, average of last 3 seasons",
    "last_gd_per_game": "goal difference last season",
    "last_gf_vs_avg": "goals scored last season",
    "last_ga_vs_avg": "goals conceded last season",
    "last_pim_vs_avg": "penalty minutes last season",
    "last_pp_pct": "power-play % last season",
    "last_pk_pct": "penalty-kill % last season",
    "roster_pts_vs_avg": "players' points last season",
    "roster_goalie_ga_vs_avg": "goalies' goals conceded last season",
    "roster_change_vs_avg": "roster change (players in minus out)",
    "new_coach": "new coach this season",
    "gf_vs_avg": "goals scored",
    "ga_vs_avg": "goals conceded",
    "pim_vs_avg": "penalty minutes",
    "pp_pct": "power-play %",
    "pk_pct": "penalty-kill %",
    "pts_vs_avg": "points",
    # coaches
    "pts_vs_usual": "last season below/above usual level",
    "coach_seasons": "seasons the coach has been at the club",
    "last_coach_win_pct": "coach's win % last season",
    "last_coach_reg_win_pct": "coach's regular-season win % last season",
    "last_coach_po_win_pct": "coach's playoff win % last season",
    "last_season_coaches": "number of coaches last season",
    "last_made_playoffs": "made the playoffs last season",
    # players
    "PIM_1": "penalty minutes last season",
    "PIM_2": "penalty minutes 2 seasons ago",
    "PIM_3": "penalty minutes 3 seasons ago",
    "GP_1": "games last season",
    "GP_2": "games 2 seasons ago",
    "GP_3": "games 3 seasons ago",
    "rate_1": "penalty minutes per game last season",
    "career_rate": "career penalty minutes per game",
    "marcel_rate_vs_league": "Marcel's rate (vs league)",
    "games_guess": "Marcel's games guess",
    "pts_rate_1": "points per game last season",
    "seasons_before": "earlier NHL seasons",
    "first_season": "first NHL season",
    "pos_C": "position: centre",
    "pos_D": "position: defence",
    "pos_L": "position: left wing",
    "pos_R": "position: right wing",
    "pos_G": "position: goalie",
    "team_style_last": "team's penalty minutes last season",
    "league_rate_last": "league penalty minutes per game last season",
}


def nice(name):
    """Plain name of a column (falls back to the column name)."""
    return LABELS.get(name, name)


def footnote(fig, text, y=-0.03):
    """Small grey line under the plot: what each mark is, and the data used.
    y = vertical position in figure coordinates (lower it if it overlaps the x-axis label)."""
    fig.text(0.01, y, text, fontsize=8.5, color="dimgrey", ha="left", va="top")
