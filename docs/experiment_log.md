# Experiment log

Every modeling attempt, in order: the goal (why we tried it), what we did, the result, and the decision. All results use the same test: 9 test seasons (2000–2009, no 2004), each predicted only from earlier seasons (`src/evaluation.py`). "Significant" = Wilcoxon p below 0.05 against the stated baseline.

## Task (a): ranking

| # | Goal | What we did | Result | Decision |
|---|---|---|---|---|
| A1 | Know what "good" means | Random order and same order as last season (per division) | Random 1.55, simple guess 1.07 positions off | Simple guess is the baseline to beat |
| A2 | Beat the simple guess with a model | Linear (3 and all inputs) and random forest, learning relative position `rank / div_size` | Linear 3 inputs 1.02; all inputs 1.07; forest 1.07 | Keep linear; fewer inputs did better (overlapping inputs) |
| A3 | Choose fairly, without looking at the test season | Practice test (last 3 training seasons) chooses the version before each season | Linear chose 3 inputs in 9/9 seasons: 1.02, p = 0.16 | 1.02 is honest; not proven |
| A4 | Check for memorising | Training vs test error | First forest: 0.57 training vs 1.07 test (overfitting); limited trees (leaf 20–40, depth 3–6): 1.02 vs 1.07 | Limit tree detail with the practice test |
| A5 | Add information that explains changes from last season | 3-season average, roster change, new coach; practice test chooses | 0.985 (first below 1), 6/2/1 better/equal/worse, p = 0.08 | Promising, not proven; fragile (1.04 with the inputs fixed) |
| A6 | Try model types with different ways of learning | Tree, kNN, gradient boosting, linear with 5 inputs | Linear 1.04, kNN 1.07, boosting 1.07 (training 0.84: memorises), tree 1.14 | None beats linear; none proven |
| A7 | Understand the models | Tree drawn, permutation importance | Last season's points +0.22 positions off when scrambled, 3-season average +0.09, rest ≈ 0 | Last season says most of what is known |
| A8 | Follow the professor's clarification | Rank per conference with the NHL rules (division winners first); models predict points | Random 4.87, simple guess 3.33 | New baseline; all (a) results redone |
| A9 | Use a better sign of real strength | Linear + last season's goal difference | 3.16, 6/2/1, p = 0.27 | Best for (a); not proven |
| A10 | Model types again, per conference | Tree, kNN, boosting with practice test | kNN 3.18, boosting 3.20, tree 3.37; no memorising | No model type proven better: the limit is pre-season information |
| A11 | How much data is needed? | Learning curve: last 1–20 seasons or all | Flat (3.13–3.20) | 1979 start is more than enough for a 3-input linear model |
| A12 | Show overfitting and the effect of a setting | Tree depth 1–12 | Best depth 3; depth 12: 1.3 training vs 3.9 test | Shallow trees only |

## Task (b): coach change

| # | Goal | What we did | Result | Decision |
|---|---|---|---|---|
| B1 | Baseline | New coach if the team missed the playoffs | Accuracy 0.57; recall 56%, precision 26%; AUC 0.56 | Use AUC for all, because only 26% are changes |
| B2 | First model | Logistic regression, 4 inputs (tenure, last coach win %, last points, coaches last season), class weights | AUC 0.62, 6/9 better, p = 0.20 | Not proven; look for better inputs |
| B3 | Use what the data understanding showed (coach plot: no changes above 70% playoff wins) | + made playoffs; + coach playoff win % | 0.61; 0.60 | No gain alone |
| B4 | Capture "worse than expected", not just "bad" | + `pts_vs_usual` (last season minus 3-season average) | 0.69, 8/9, p = 0.012 | First significant result |
| B5 | Separate playoff and regular-season success | "split win%" set | 0.67, 9/9, p = 0.004 | Kept as a candidate |
| B6 | Choose fairly between sets | Practice test chooses the set before each season | 0.68, 8/9, p = 0.012 | Final (b) model |
| B7 | Do more flexible models help? | Random forest and gradient boosting on the "split win%" set | 0.645 (8/9), 0.640 (6/9) | Logistic stays; more flexibility does not help with ~700 team-seasons. Quick test outside the notebooks: Person 2 adds these models to notebook 03 |
| B8 | Catch more real changes (missing one is worse) | Cut-off chosen by the practice test with recall counted double (F2) | Recall 90% (simple guess 56%), precision 26%, says "yes" for 75% | Matches the business goal; trade-off stated |
| B9 | Check memorising and what matters | Training vs test AUC; permutation importance | 0.69 vs 0.67; below usual level −0.12 AUC when scrambled, then coaches last season, coach playoff win % | No overfitting; interpretation fits hockey |

## Task (c): penalty minutes

| # | Goal | What we did | Result | Decision |
|---|---|---|---|---|
| C1 | Baselines from no information to hockey knowledge | Median, position average, same as last season, Marcel | 27.3, 29.0, 18.4, 17.2 minutes off | Marcel is the baseline to beat |
| C2 | Know the ceiling | Last rate × this season's real games (not allowed) | 14.0 | Unknown games played is the main limit |
| C3 | Beat Marcel | Linear, tree, kNN, gradient boosting (absolute error), practice test for settings | Boosting 16.5 (9/9, p = 0.004); tree 17.3; linear 17.6; kNN 17.9 | Final (c) model: gradient boosting with absolute error |
| C4 | Check memorising and what matters | Training MAE on 2006–08; permutation importance | 15.4 vs 16.5 test: small gap; last season's PIM, then career rate | No overfitting |
| C5 | Deal with the skewed target in another way | Learn log(1 + PIM) with squared-error models | Boosting 17.8 → 17.1; linear 17.6 → 18.7 | Log helps flexible models, hurts linear; keep absolute error |
| C6 | How much data is needed? | Learning curve: last 1–20 seasons or all | 17.4 with 1 season, 16.6 with 10, flat after | Boosting needs about 10 seasons; 1979 start is enough |
| C7 | Show overfitting and the effect of a setting | Tree depth 1–16 | Best depth about 6; depth 16: 8.9 training vs 23.9 test | Depth must be limited |
