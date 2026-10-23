"""Season-by-season testing, shared by task (a) and task (b).

For each test season we pretend to be the day before it starts:
the model may only learn from the seasons before it, then predicts that season.
"""
import pandas as pd


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
    """On average, how many positions off the predicted rank is (0 = perfect)."""
    return (test["rank"] - pd.Series(list(predicted_rank), index=test.index)).abs().mean()
