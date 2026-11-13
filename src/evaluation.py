"""Season-by-season testing, shared by tasks (a), (b) and (c).

For each test season we pretend to be the day before it starts:
the model may only learn from the seasons before it, then predicts that season.
"""
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score


def test_seasons(table, n=9):
    """The last n seasons in the table (2004 is not in the data, so 2000-2009 gives 9)."""
    return [int(y) for y in sorted(table["year"].unique())[-n:]]


def evaluate_by_season(table, predict, score, seasons):
    """Run `predict` once per season and score it.

    predict(train, test) -> predictions for the rows of `test`
        train = all rows from seasons before the test season
        test  = the rows of the test season
    score(test, predictions) -> one number

    Returns a table with one row per season, so we can see the score of each season
    and its average.
    """
    results = []
    for season in seasons:
        train = table[table["year"] < season]
        test = table[table["year"] == season]
        predictions = predict(train, test)
        results.append({"season": season, "score": score(test, predictions)})
    return pd.DataFrame(results)


# ---------- Task (a): ranking ----------

def division_rank(test, strength):
    """Turn any 'how strong is this team' number into a position 1, 2, 3... inside each division.
    Higher strength = better position. Teams with no value go last."""
    s = pd.Series(list(strength), index=test.index)
    return s.groupby([test["year"], test["divID"]]).rank(ascending=False, method="first", na_option="bottom")


def mean_rank_error(test, predicted_rank):
    """On average, how many positions off the predicted division rank is (0 = perfect)."""
    return (test["rank"] - pd.Series(list(predicted_rank), index=test.index)).abs().mean()


def division_winner_places(year):
    """How many top places in each conference go to division winners (NHL rules):
    1979-1992: none (conference order is by points only)
    1993-1997: 2 (the 2 division winners are 1st and 2nd)
    1998-2009: 3 (the 3 division winners are 1st, 2nd and 3rd)"""
    if year < 1993:
        return 0
    return 2 if year < 1998 else 3


def conference_rank(test, strength):
    """Turn any 'how strong is this team' number into a position 1, 2, 3... inside each conference,
    following the NHL rules: division winners first (see division_winner_places), then the
    other teams. Higher strength = better position. Teams with no value go last.

    For the real ranking, use strength = points, with wins and goal difference as tie-breakers
    (see true_strength). For a prediction, use the predicted points."""
    s = pd.Series(list(strength), index=test.index).fillna(-np.inf)
    ranks = pd.Series(np.nan, index=test.index)
    for (year, conf), g in test.groupby(["year", "confID"]):
        strength_g = s.loc[g.index].sort_values(ascending=False, kind="stable")
        winners = []
        if division_winner_places(year) > 0:
            # the strongest team of each division
            best_per_div = g.loc[strength_g.index].groupby("divID", sort=False).head(1).index
            winners = list(strength_g.loc[best_per_div].sort_values(ascending=False, kind="stable").index)
        others = [i for i in strength_g.index if i not in winners]
        order = winners + others
        ranks.loc[order] = range(1, len(order) + 1)
    return ranks


def true_strength(teams):
    """Real end-of-season strength: points first, then wins, then goal difference.
    Reproduces 99.5% of the division ranks in Teams.csv 1979-2009 (the rest were
    head-to-head tie-breaks, which we cannot compute)."""
    return teams["Pts"] + teams["W"] / 1e3 + (teams["GF"] - teams["GA"]) / 1e6


def mean_conference_rank_error(test, predicted_rank):
    """On average, how many positions off the predicted conference rank is (0 = perfect).
    Needs the real conference rank in column `conf_rank`."""
    return (test["conf_rank"] - pd.Series(list(predicted_rank), index=test.index)).abs().mean()


# ---------- Task (b): coach changes ----------

def coach_auc(test, probabilities):
    """AUC of the predicted chance of a coach change (0.5 = coin flip, 1 = perfect).
    Teams without an answer (new teams) are left out."""
    actual = pd.to_numeric(test["coach_change"], errors="coerce")
    valid = actual.notna()

    actual = actual[valid].astype(int)
    probabilities = pd.Series(
        probabilities, index=test.index
    )[valid]

    if actual.nunique() < 2:
        return np.nan

    return roc_auc_score(actual, probabilities)


# ---------- Task (c): penalty minutes ----------

def pim_mae(test, predictions):
    """On average, how many penalty minutes off the prediction is (0 = perfect)."""
    return (test["PIM"] - pd.Series(list(predictions), index=test.index)).abs().mean()


# ---------- Choosing settings fairly ----------

def pick_with_practice_test(train, candidates, score, n_practice=3, lower_is_better=True):
    """Choose one of several candidate predict functions using only the training seasons.

    candidates = {"name": predict(train, test), ...}
    The last `n_practice` training seasons become a practice test: each candidate learns from
    the seasons before them, predicts them, and gets the average score. Returns the name of the
    best candidate and all practice scores. The real test season is never looked at.
    """
    seasons = sorted(train["year"].unique())
    practice = seasons[-n_practice:]
    inner = train[train["year"] < practice[0]]
    results = {}
    for name, predict in candidates.items():
        scores = [score(train[train["year"] == s], predict(inner, train[train["year"] == s])) for s in practice]
        results[name] = sum(scores) / len(scores)
    best = min(results, key=results.get) if lower_is_better else max(results, key=results.get)
    return best, results
