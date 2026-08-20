# ============================================================
# BLOCK 1: Load libraries and data
# ============================================================

# Load the tidyverse package (gives us dplyr for data manipulation and ggplot2 for plotting, among other things)
library(tidyverse)

# Read in the CSV we exported from Python.
patents <- read_csv("../data/patents_with_domains.csv")

head(patents)
glimpse(patents)


# ============================================================
# BLOCK 2: Basic cleanup
# ============================================================

# Convert year to a clean integer
patents <- patents %>%
  mutate(Year = as.integer(Year))

patents %>%
  count(domain, sort = TRUE)


# ============================================================
# BLOCK 3: Novelty by domain by year (the core trend table)
# ============================================================

# For each domain-year combination, calculate:
#   - average Novelty score
#   - number of patents (volume)
novelty_by_domain_year <- patents %>%
  group_by(domain, Year) %>%
  summarise(
    avg_novelty = mean(Novelty, na.rm = TRUE),
    patent_count = n(),
    .groups = "drop"
  )

print(novelty_by_domain_year, n = 50)


# ============================================================
# BLOCK 4: Trend slope per domain (is Novelty rising or falling?)
# ============================================================

# For each domain, fit a simple linear model of avg_novelty ~ Year
# The slope tells us the direction/steepness of the trend.
# A positive slope = novelty rising over time in that domain.
# A negative slope = novelty falling.

trend_slopes <- novelty_by_domain_year %>%
  group_by(domain) %>%
  summarise(
    slope = coef(lm(avg_novelty ~ Year))[["Year"]],
    total_patents = sum(patent_count)
  ) %>%
  arrange(desc(slope))   # sort so the fastest-rising domain is at the top

print(trend_slopes)


# ============================================================
# BLOCK 5: Chart 1 — Novelty trend by domain over time (line chart)
# ============================================================

novelty_trend_plot <- ggplot(novelty_by_domain_year, aes(x = Year, y = avg_novelty, color = domain)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  labs(
    title = "Average Patent Novelty Score by Domain (2016–2020)",
    subtitle = "Higher score = more novel/unexpected combination of technical elements",
    x = "Year",
    y = "Average Novelty Score",
    color = "Domain"
  ) +
  theme_minimal()

# Display it in RStudio's Plots panel
novelty_trend_plot

# Save it as a PNG
ggsave("../output/novelty_trend_by_domain.png", novelty_trend_plot, width = 10, height = 6, dpi = 300)


# ============================================================
# BLOCK 6: Chart 2 — Patent volume by domain (bar chart)
# ============================================================

# Total patents per domain across the whole period, sorted largest to smallest
volume_by_domain <- patents %>%
  count(domain, sort = TRUE)

volume_plot <- ggplot(volume_by_domain, aes(x = reorder(domain, n), y = n)) +
  geom_col(fill = "steelblue") +
  coord_flip() +   # horizontal bars — easier to read domain names
  labs(
    title = "Total Patent Volume by Domain (2016–2020)",
    x = "Domain",
    y = "Number of Patents"
  ) +
  theme_minimal()

volume_plot

ggsave("../output/volume_by_domain.png", volume_plot, width = 10, height = 6, dpi = 300)


# ============================================================
# BLOCK 7: Export the summary tables
# ============================================================

# Save these as CSVs
write_csv(novelty_by_domain_year, "../output/novelty_by_domain_year.csv")
write_csv(trend_slopes, "../output/trend_slopes.csv")