# Task (c), data understanding in R: player types and penalty minutes by position.
# Base R only (no packages to install). Run from the project folder:  Rscript R/player_types.R
# Same analysis as notebooks/01_data_overview.ipynb, section "Player types", to check it with a second tool.

players <- read.csv("data/player_table.csv")
players$pim_per_game <- players$PIM / players$GP
players$pts_per_game <- players$Pts / players$GP
regular <- subset(players, GP >= 20)                  # rates only for players with 20+ games

# 1. Penalty minutes per game by position: Kruskal-Wallis (rank test, PIM is skewed)
cat("Median PIM per game by position:\n")
print(round(tapply(regular$pim_per_game, regular$pos, median), 2))
kw_all <- kruskal.test(pim_per_game ~ factor(pos), data = regular)
kw_skaters <- kruskal.test(pim_per_game ~ factor(pos), data = subset(regular, pos != "G"))
cat(sprintf("Kruskal-Wallis, all positions: chi-squared = %.0f, p = %.1e\n", kw_all$statistic, kw_all$p.value))
cat(sprintf("Kruskal-Wallis, skaters only:  chi-squared = %.0f, p = %.1e\n\n", kw_skaters$statistic, kw_skaters$p.value))

# 2. Player types: k-means on 3 scaled variables (same as the Python notebook)
skaters <- subset(regular, pos != "G")
skaters$pim_vs_league <- skaters$pim_per_game / skaters$league_rate
X <- scale(skaters[, c("pim_vs_league", "pts_per_game", "GP")])
set.seed(0)
km <- kmeans(X, centers = 4, nstart = 10, iter.max = 100)
skaters$type_id <- km$cluster

# Name the groups from their medians (hockey reading of the numbers)
med <- aggregate(cbind(pim_vs_league, pts_per_game, GP) ~ type_id, data = skaters, FUN = median)
type_name <- rep(NA_character_, 4)
type_name[med$type_id[which.max(med$pim_vs_league)]] <- "enforcer"
type_name[med$type_id[which.max(med$pts_per_game)]] <- "scorer"
rest <- med[is.na(type_name[med$type_id]), ]
type_name[rest$type_id[which.min(rest$GP)]] <- "part-timer"
type_name[is.na(type_name)] <- "regular"
skaters$player_type <- type_name[skaters$type_id]

summary_t <- aggregate(cbind(pim_vs_league, pts_per_game, GP, PIM) ~ player_type, data = skaters, FUN = median)
summary_t$player_seasons <- as.vector(table(skaters$player_type)[summary_t$player_type])
cat("Player types (k-means, k = 4, medians):\n")
print(summary_t, digits = 3, row.names = FALSE)

# 3. Plot with 4 variables: x = points per game, y = PIM per game vs league,
#    point size = games played, colour = player type
colours <- c("enforcer" = "#d62728", "scorer" = "#2ca02c", "regular" = "#1f77b4", "part-timer" = "#7f7f7f")
set.seed(0)
sample_rows <- skaters[sample(nrow(skaters), 4000), ]
dir.create("figures", showWarnings = FALSE)
png("figures/player_types_R.png", width = 1600, height = 1200, res = 160)
plot(sample_rows$pts_per_game, sample_rows$pim_vs_league,
     col = adjustcolor(colours[sample_rows$player_type], alpha.f = 0.5), pch = 16,
     cex = sample_rows$GP / 45,
     xlab = "points per game", ylab = "PIM per game vs league (1 = league average)",
     main = "Player types in R (k-means, k = 4)\npoint size = games played; skaters with 20+ games, 1979-2009")
legend("topright", legend = names(colours), col = colours, pch = 16, pt.cex = 1.5, bty = "n")
invisible(dev.off())
cat("\nSaved figures/player_types_R.png\n")
