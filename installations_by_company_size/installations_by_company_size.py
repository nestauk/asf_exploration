# %% [markdown]
# ## Number of installations by company size over time
#
# This notebook contains analysis to understand the counts and proportions of heat pumps installed by differently sized companies. We have used the MCS installations data, using annual installations per company, to produce a proxy for this. The research questions to answer are as follows:
# 1. Which companies are the top 30 installers in Q1 2025 by installation count?
# 2. Which companies are the top 10 installers in 2024 by installation count?
# 3. What are the proportions of installations by differently sized companies over time?
# 4. What are the counts of installations by differently sized companies over time?
# 5. What is the breakdown of the number of companies per size bracket in 2024?
#
# This analysis uses the processed MCS installations data up to and including Q1 2025.

# %%
import polars as pl
import matplotlib.pyplot as plt
import numpy as np

# %%
installations_df = pl.read_parquet("s3://asf-daps/lakehouse/2025_Q1/processed/mcs/mcs_installations_250611-0.parquet")

# %%
installations_df = installations_df.drop("__index_level_0__").filter(
    # Check if we want to include any other installation_type fields
    pl.col("installation_type") == "Domestic",
    pl.col("tech_type") != "Micro CHP",
).with_columns(
    # Drop duplicate rows - check that we should do this. Could these represent true multi-installs?
    pl.col(pl.String).str.to_lowercase()
).unique()

# %%
# This is to ensure the ranges show in the desired order on the plots
order_of_ranges = {
    "1-10": 0,
    "11-50": 1,
    "51-100": 2,
    "101-365": 3,
    "Over 365": 4
}

# %%
# Aggregate the number of installations per installer company per year
installations_per_installer_per_year = installations_df.group_by(["company_unique_id", "commission_year"]).len().rename({"len": "n_installations"}).with_columns(
    (pl.col("n_installations") / pl.col("n_installations").sum().over("commission_year")).alias("proportion_of_total_installations_per_year"),
    # Add ranges
    pl.when(pl.col("n_installations") <= 10)
    .then(pl.lit("1-10"))
    # Both ends inclusive
    .when(pl.col("n_installations").is_between(11, 50, closed="both"))
    .then(pl.lit("11-50"))
    .when(pl.col("n_installations").is_between(51, 100, closed="both"))
    .then(pl.lit("51-100"))
    .when(pl.col("n_installations").is_between(101, 365, closed="both"))
    .then(pl.lit("101-365"))
    .when(pl.col("n_installations") > 365)
    .then(pl.lit("Over 365"))
    .otherwise(pl.lit("error"))
    .alias("n_installations_range")
).with_columns(
    pl.col("n_installations_range").replace(order_of_ranges).cast(pl.Int8).alias("range_order")
).sort(by="range_order", descending=False)

# %%
# Top 30 installers in 2025 Q1
installations_per_installer_per_year.filter(pl.col("commission_year") == 2025).with_columns(
    (pl.col("proportion_of_total_installations_per_year") *100).round(3).alias("pc_of_total_installations_per_quarter")
).sort(by="n_installations", descending=True).head(30).drop(["proportion_of_total_installations_per_year", "range_order", "n_installations_range"]).write_csv("top30_installers_q1_2025.csv")

# Remove 2025 data for the rest of the analysis because we don't have a full year
installations_per_installer_per_year = installations_per_installer_per_year.filter(pl.col("commission_year") != 2025)

# %%
# Top 10 installers in 2024
installations_per_installer_per_year.filter(pl.col("commission_year") == 2024).with_columns(
    (pl.col("proportion_of_total_installations_per_year") *100).round(3).alias("pc_of_total_installations_per_year")
).sort(by="n_installations", descending=True).head(10).drop(["proportion_of_total_installations_per_year", "range_order", "n_installations_range"])

# %%
# Aggregate the number of installations per 'size' of installer company per year
installations_per_size_per_year = installations_per_installer_per_year.group_by(["n_installations_range", "commission_year"]).agg(
    pl.col("n_installations").sum(),
    pl.col("range_order").first(),
    pl.col("company_unique_id").n_unique().alias("n_companies")
).with_columns(
    (pl.col("n_installations") / pl.col("n_installations").sum().over(["commission_year"])).alias("proportion_of_total_installations_per_year")
).sort(by=["range_order", "commission_year"])

# %%
# Show the proportions of installations by each group over time
commission_years = installations_per_size_per_year["commission_year"].unique().sort()

# colour_map = {r: colour for r in order_of_ranges}
def create_colour_map(cmap, n):
    cm = plt.get_cmap(cmap)
    pts = np.linspace(0, 1, n)
    return [cm(pt) for pt in pts]

colours = create_colour_map("viridis", len(order_of_ranges))

fig = plt.figure(figsize=(12, 5))

# Plot each time series
for r, colour in zip(order_of_ranges, colours):
    plot_data = installations_per_size_per_year.filter(pl.col("n_installations_range") == r)
    plt.plot(plot_data["commission_year"], plot_data["proportion_of_total_installations_per_year"], color=colour, label=r)

plt.title("Proportion of annual domestic heat pump installations by company installation count")
plt.xlabel("Year")
plt.ylabel("Proportion of total annual installations")
plt.legend(title="Number of annual installations per company*")
plt.xticks(commission_years)

text = "*The groups represent the number of installations per year per company. " \
"The lines in the plot will therefore represent different total numbers of companies in different years as the number of installations by individual companies grows."
plt.figtext(
    0.5, -0.06, text, wrap=True, horizontalalignment="center"
)

# %%
# Show the count of installations over time
commission_years = installations_per_size_per_year["commission_year"].unique().sort()

colours = create_colour_map("viridis", len(order_of_ranges))

fig = plt.figure(figsize=(12, 5))

for r, colour in zip(order_of_ranges, colours):
    plot_data = installations_per_size_per_year.filter(pl.col("n_installations_range") == r)
    plt.plot(plot_data["commission_year"], plot_data["n_installations"], color=colour, label=r)

plt.title("Count of annual domestic heat pump installations by company installation count")
plt.xlabel("Year")
plt.ylabel("Count of total annual installations")
plt.legend(title="Number of annual installations per company*")
plt.xticks(commission_years)

text = "*The groups represent the number of installations per year per company. " \
"The lines in the plot will therefore represent different total numbers of companies in different years as the number of installations by individual companies grows."
plt.figtext(
    0.5, -0.06, text, wrap=True, horizontalalignment="center"
)

# %%
# Show the counts of companies in each bracket over time
commission_years = installations_per_size_per_year["commission_year"].unique().sort()

colours = create_colour_map("viridis", len(order_of_ranges))

fig = plt.figure(figsize=(12, 5))

for r, colour in zip(order_of_ranges, colours):
    plot_data = installations_per_size_per_year.filter(pl.col("n_installations_range") == r)
    plt.plot(plot_data["commission_year"], plot_data["n_companies"], color=colour, label=r)

plt.title("Count of installer companies by number of annual installations per year")
plt.xlabel("Year")
plt.ylabel("Count of installer companies")
plt.legend(title="Number of annual installations per company*")
plt.xticks(commission_years)
plt.show()

# %%
# Breakdown of companies per bracket in 2024
installations_per_size_per_year.filter(pl.col("commission_year") == 2024).with_columns(
    (pl.col("n_companies") / pl.col("n_companies").sum() * 100).alias("pc_of_companies")
).select(
    ['n_installations_range',
 'commission_year',
 'n_installations',
 'n_companies',
 'pc_of_companies']
)
