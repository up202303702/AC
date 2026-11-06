# Modeling, explained simply

What we did for task (a), why the results are inconclusive, and what to do next. Code: `notebooks/03_modeling.ipynb`. Short version of the numbers: `docs/project_notes.md`, section *Modeling*.

## 1. What a "model" does here

A model looks at past seasons and learns a rule like *"teams that did well last season and have strong players usually finish high"*. Then it applies that rule to a new season.

For every team it gives one number: **how high we expect it to finish in its division**, from 0 (top) to 1 (bottom). We use this scale instead of the position itself because divisions had 4 to 7 teams, so "5th" can mean last or middle.

Then, inside each division, the teams are put in order of that number: lowest number = 1st, next = 2nd, and so on. That is our predicted ranking.

## 2. How we test a model

We pretend to be the day before each season from 2000 to 2009:

1. The model may only learn from the seasons **before** that season.
2. It predicts the ranking of that season.
3. We count how many positions off it was, on average.

We do this for all 9 seasons (2004 does not exist) and take the average. This is fair: the model never sees the season it predicts, just like in real life.

## 3. What we compared

| What | How it works | Positions off (average) |
|---|---|---|
| Random order | Teams in a random order | 1.55 |
| Simple guess | Same order as last season | 1.07 |
| Linear model, 3 inputs | A weighted sum of last season's points, the players' points and the goalies' goals conceded | **1.02** |
| Linear model, all 9 inputs | Same, with every column we have | 1.07 |
| Random forest | 300 "decision trees" (chains of yes/no questions) that vote | 1.07 |

What the linear model learned makes hockey sense: a good last season counts the most; strong players help a little; goalies who conceded a lot hurt a little.

## 4. Why the results are inconclusive

All models are **much better than random**, but **not clearly better than the simple guess**. Three reasons:

**Reason 1: last season already says most of what can be known.** A team that was good last season usually stays good, and the simple guess already uses that. What changes during a season (injuries, trades, luck in close games) is not in any data we have before the season starts. So there is little room left to improve.

**Reason 2: the difference is too small to be sure it is real.** 1.07 vs 1.02 is a difference of 0.05 positions per team. With about 30 teams in a season, that is roughly **one or two teams guessed one place better per season**. That can happen by luck. We checked with a statistical test (Wilcoxon), which asks: *"if the model were no better at all, how often would we see a difference this big just by chance?"* The answer was 16% of the time. The usual bar is 5%, so we cannot rule out luck. With only 9 test seasons, proving a small difference is hard.

**Reason 3: the extra inputs mostly repeat each other.** Last season's points and last season's rank say almost the same thing, and so do last season's goals conceded and the goalies' record. Adding them gives the model nothing new, only more chances to pick up noise. That is why "all 9 inputs" is not better than "3 inputs".

## 5. The random forest: what "overfitting" means

We measured each model's error twice:

| Model | Error on the seasons it learned from | Error on new seasons |
|---|---|---|
| Linear, 3 inputs | 1.08 | 1.02 |
| Linear, all inputs | 1.09 | 1.07 |
| Random forest | **0.57** | **1.07** |

The forest is very good on the seasons it learned from (0.57) but no better than the simple guess on new seasons (1.07). That means it **memorised** the training seasons, including their luck, instead of learning a rule that works on new ones. This is called **overfitting**: like a student who memorises last year's exam answers and then fails a new exam.

The linear models have almost the same error on both, so they are **not** overfitting. They learned a simple rule that carries over.

**What we did about it:** we made the forest's trees less detailed (each final answer must be based on at least 20 or 40 teams, and a tree may ask at most 3 or 6 questions in a row) and let the practice test below choose how detailed. The memorising stopped: 1.02 on the seasons it learned from, 1.07 on new ones. But it is **still no better than the simple guess**, and the chosen setting changes from season to season, so no forest setting is clearly better. This supports reason 1: the limit is the information we have before the season, not the model.

## 6. Choosing fairly: the practice test

At first we tried three versions and reported the best **after seeing the test results**, which makes the winner look slightly better than it is. Now each version is chosen **inside the training seasons only**: the last 3 training seasons are a "practice test", the version with the best practice score is chosen, and only then is it scored on the real test season. The real test season is never used to decide anything.

Result: for the linear model the practice test chose **3 inputs in all 9 seasons**, so its 1.02 is an honest number. The forest's choice changed every few seasons and stayed at 1.07.

| Model (chosen fairly) | Error on seasons it learned from | Error on new seasons | Seasons better / equal / worse than the simple guess | Could it be luck? (Wilcoxon) |
|---|---|---|---|---|
| Linear | 1.08 | **1.02** | 5 / 3 / 1 | 16% chance: not proven |
| Forest | 1.02 | 1.07 | 5 / 1 / 3 | 98% chance: no real difference |

## 6b. New inputs: can we predict changes from last season?

We added three inputs that might explain why a team does better or worse than last season:

- **3-season average:** one great season can be luck; three are not.
- **Roster change:** points of the players who arrived minus those of the players who left.
- **New coach this season:** known before the season, so allowed here.

The practice test chose between them before each season. Result: **0.985 positions off**, the first result below 1, better than the simple guess in 6 of 9 seasons. The chance that this is luck is 8%: closer to the 5% bar, but still not proven. The new coach and the 3-season average were chosen; roster change never was, because it hardly relates to where teams finish.

**But careful:** that 0.985 came from the practice test switching inputs from season to season. With the same 5 inputs every season, the linear model scores 1.04. So the gain is fragile.

## 6c. Other kinds of model

We tried three more ways of learning, all with the same inputs and the practice test choosing their settings:

- **Decision tree:** a chain of yes/no questions. 1.14: worse than the simple guess, but easy to read (`figures/decision_tree_a.png`). It first asks *"was last season's points above 1.09 of the average?"*, then looks at the 3-season average and the goalies.
- **k-nearest neighbours:** looks for the 25 most similar past teams and copies how they finished. 1.07: same as the simple guess.
- **Gradient boosting:** many small trees, each fixing the previous one's mistakes. 1.07, and it memorises a bit (0.84 on the seasons it learned from).

None beats the linear model, and none is proven better than the simple guess.

**Which inputs matter** (`figures/feature_importance_a.png`): we scramble one input at a time and see how much worse the predictions get. Last season's points: +0.22 positions off when scrambled, by far the most. 3-season average: +0.09. Players and goalies: a little. New coach: nothing.

## 7. What to say if asked

- "Predicting the final ranking before the season is hard: last season explains most of it, and the rest is in-season events we cannot see."
- "Our models beat random clearly, but beat the simple guess only slightly, and with 9 test seasons that difference is not statistically proven."
- "The first random forest overfitted; with less detailed trees, chosen fairly, it stopped overfitting but still did not beat the simple guess."

## 8. Next steps

1. Try other model types (a single decision tree we can show on a slide, k-nearest neighbours, gradient boosting), chosen with the practice test.
2. Keep only inputs that add new information.
3. Do the same for task (b) once the coach table exists (the practice test is in `src/evaluation.py`, ready to reuse).
