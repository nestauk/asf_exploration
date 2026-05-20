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
raw_installations_df = pl.read_parquet("s3://asf-daps/lakehouse/2025_Q1/processed/mcs/mcs_installations_250611-0.parquet")

# %%
raw_installations_df["installation_type"].value_counts()

# %%
installations_df = raw_installations_df.drop("__index_level_0__").filter(
    # Check if we want to include any other installation_type fields
    pl.col("installation_type") == "Domestic",
    pl.col("tech_type") != "Micro CHP",
).with_columns(
    # Drop duplicate rows - check that we should do this. Could these represent true multi-installs?
    pl.col(pl.String).str.to_lowercase()
).unique()

# %%
# This is to ensure the ranges show in the desired order on the plots
# The buckets were selected based on manual inspection of the distribution of installations in 2024 and then sense-checked with the team
order_of_ranges = {
    "1-10": 0,
    "11-50": 1,
    "51-100": 2,
    "101-365": 3,
    "Over 365": 4
}

# %%
# Aggregate the number of installations per installer company per year

# Add ranges - both ends inclusive
range_labels = ["1-10", "11-50", "51-100", "101-365", "Over 365"]
range_breaks = [10, 50, 100, 365]

installations_per_installer_per_year = (
    installations_df.group_by(["company_unique_id", "commission_year"])
    .len()
    .rename({"len": "n_installations"})
    .with_columns(
        (pl.col("n_installations") / pl.col("n_installations").sum().over("commission_year"))
        .alias("proportion_of_total_installations_per_year"),
        pl.col("n_installations").cut(breaks=range_breaks, labels=range_labels).alias("n_installations_range"),
    )
    .with_columns(
        pl.col("n_installations_range").replace(order_of_ranges).cast(pl.Int8).alias("range_order"),
        pl.col("n_installations_range").cast(pl.String)
    )
    .sort(by="range_order", descending=False)
)

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
).sort(by="n_installations", descending=True).head(10).drop(["proportion_of_total_installations_per_year", "range_order", "n_installations_range"]).write_csv("top10_installers_2024.csv")

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
# Show the proportions of installations by each group over time - line chart
commission_years = np.arange(2013, 2025, 1)

def create_colour_map(cmap, n):
    cm = plt.get_cmap(cmap)
    pts = np.linspace(0, 1, n)
    return [cm(pt) for pt in pts]

colours = create_colour_map("viridis", len(order_of_ranges))

fig = plt.figure(figsize=(12, 5))

# Plot each time series
for r, colour in zip(order_of_ranges, colours):
    plot_data = installations_per_size_per_year.filter(pl.col("n_installations_range") == r, pl.col("commission_year") >= 2013)
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
# Show proportions of installations by each group over time - same as above as area chart
installations_per_size_per_year_from_2013 = installations_per_size_per_year.filter(pl.col("commission_year") >= 2013)

proportions_wide = (
    installations_per_size_per_year_from_2013
    .pivot(
        on="n_installations_range",
        index="commission_year",
        values="proportion_of_total_installations_per_year",
    )
    .fill_null(0)
    .sort("commission_year")
)

commission_years = proportions_wide["commission_year"].to_numpy()
stacked_proportions = [proportions_wide[r].to_numpy() for r in order_of_ranges]

fig = plt.figure(figsize=(12, 5))

plt.stackplot(
    commission_years,
    stacked_proportions,
    colors=colours,
    labels=list(order_of_ranges),
)

plt.title("Proportion of annual domestic heat pump installations by company installation count")
plt.xlabel("Year")
plt.ylabel("Proportion of total annual installations")
plt.legend(title="Number of annual installations per company*", loc="upper left", bbox_to_anchor=(1.02, 1))
plt.xticks(commission_years)
plt.xlim(commission_years.min(), commission_years.max())
plt.ylim(0, 1)

text = "*The groups represent the number of installations per year per company. " \
"The lines in the plot will therefore represent different total numbers of companies in different years as the number of installations by individual companies grows."
plt.figtext(
    0.5, -0.06, text, wrap=True, horizontalalignment="center"
)

# %%
# Show the count of installations over time - line chart
fig = plt.figure(figsize=(12, 5))

for r, colour in zip(order_of_ranges, colours):
    plot_data = installations_per_size_per_year.filter(pl.col("n_installations_range") == r, pl.col("commission_year") >= 2013)
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
# Show count of installations over time - same as above as area chart
counts_wide = (
    installations_per_size_per_year
    .filter(pl.col("commission_year") >= 2013)
    .pivot(
        on="n_installations_range",
        index="commission_year",
        values="n_installations",
    )
    .fill_null(0)
    .sort("commission_year")
)

commission_years = counts_wide["commission_year"].to_numpy()
stacked_counts = [counts_wide[r].to_numpy() for r in order_of_ranges]

colours = create_colour_map("viridis", len(order_of_ranges))

fig = plt.figure(figsize=(12, 5))

plt.stackplot(
    commission_years,
    stacked_counts,
    colors=colours,
    labels=list(order_of_ranges),
)

plt.title("Count of annual domestic heat pump installations by company installation count")
plt.xlabel("Year")
plt.ylabel("Count of total annual installations")
plt.legend(title="Number of annual installations per company*", loc="upper left", bbox_to_anchor=(1.02, 1))
plt.xticks(commission_years)
plt.xlim(commission_years.min(), commission_years.max())

text = "*The groups represent the number of installations per year per company. " \
"The areas in the plot will therefore represent different total numbers of companies in different years as the number of installations by individual companies grows."
plt.figtext(
    0.5, -0.06, text, wrap=True, horizontalalignment="center"
)

# %%
# Show the counts of companies in each bracket over time
fig = plt.figure(figsize=(12, 5))

for r, colour in zip(order_of_ranges, colours):
    plot_data = installations_per_size_per_year.filter(pl.col("n_installations_range") == r, pl.col("commission_year") >= 2013)
    plt.plot(plot_data["commission_year"], plot_data["n_companies"], color=colour, label=r)

plt.title("Count of installer companies by number of annual installations per year")
plt.xlabel("Year")
plt.ylabel("Count of installer companies")
plt.legend(title="Number of annual installations per company")
plt.xticks(commission_years)
plt.show()

# %%
# Breakdown of companies per bracket in 2024
installations_per_size_per_year.filter(pl.col("commission_year") == 2024).with_columns(
    (pl.col("n_companies") / pl.col("n_companies").sum() * 100).round(2).alias("pc_of_companies"),
    (pl.col("n_installations") / pl.col("n_installations").sum() * 100).round(2).alias("pc_of_installations")
).select(
    ['n_installations_range',
 'commission_year',
 'n_installations',
 'n_companies',
 'pc_of_companies',
 "pc_of_installations"]
).write_csv("companies_per_bracket_in_2024.csv")
