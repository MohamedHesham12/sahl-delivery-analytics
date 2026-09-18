import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df = pd.read_csv("File 2.csv")

#-----DATA ClEANING---------

# 1. drop duplicate rows
df = df.drop_duplicates()

# 2. column more than 90% empty
df = df.dropna(thresh=len(df) * 0.1, axis=1)

# 3. number stored as text (order_value_egp)
if df["order_value_egp"].dtype == object:
    df["order_value_egp"] = df["order_value_egp"].astype(str).str.replace(
        r"[^\d.]", "", regex=True
    )
    df["order_value_egp"] = pd.to_numeric(df["order_value_egp"], errors="coerce")

# 4. The same place written many ways (Standardise zone/city names)
df["zone"] = df["zone"].astype(str).str.strip().str.title()
zone_mapping = {
    "Abu Qirqas": "Abu Qurqas",
    "Abu-Qurqas": "Abu Qurqas",
    "Aboo Qurqas": "Abu Qurqas",
    "New-Minya": "New Minya",
    "N-Minya": "New Minya",
}
df["zone"] = df["zone"].replace(zone_mapping)

# 5. Two date formats in one column
df["order_datetime"] = pd.to_datetime(
    df["order_datetime"], format="%Y-%m-%d %H:%M:%S", errors="coerce"
).fillna(
    pd.to_datetime(
        df["order_datetime"], format="%d/%m/%Y %H:%M", errors="coerce"
    )
)

# 6. physically impossible value (e.g., negative distance or actual_minutes <= 0)
df = df[
    (df["distance_km"] > 0)
    & (df["actual_minutes"] > 0)
    & (df["prep_minutes"] > 0)
]

# 7. missing NUMERIC value (fill with median)
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    if col != "customer_rating":
        df[col] = df[col].fillna(df[col].median())

# 8. Missing customer_rating: LEAVE BLANK (Do not fill)

# Checkpoint verification
print("--- Checkpoint Verification ---")
print("Shape:", df.shape)
print("Duplicates:", df.duplicated().sum())
print("Missing values:\n", df.isnull().sum())

# Feature Engineering
df["delay_minutes"] = df["actual_minutes"] - df["promised_minutes"]
df["is_late"] = (df["delay_minutes"] > 0).astype(int)
df["order_hour"] = df["order_datetime"].dt.hour


#------DASHBOARD-------

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(3, 2, figsize=(16, 18))

# Panel 1: Overall Reorder Rate vs Delay Severity
df["delay_group"] = pd.cut(
    df["delay_minutes"],
    bins=[-np.inf, 0, 10, 25, np.inf],
    labels=["On-Time/Early", "1-10m Late", "11-25m Late", "25m+ Late"],
)
reorder_by_delay = (
    df.groupby("delay_group", observed=False)["reordered_within_30d"]
    .mean()
    .reset_index()
)
sns.barplot(
    data=reorder_by_delay,
    x="delay_group",
    y="reordered_within_30d",
    ax=axes[0, 0],
    palette="Blues_r",
)
axes[0, 0].set_title("1. Retention Rate drops severely as Delays Increase")
axes[0, 0].set_xlabel("Delay Category")
axes[0, 0].set_ylabel("Reorder Rate (30 Days)")
axes[0, 0].set_ylim(0, 1)

# Panel 2: Vehicle Type vs Delay Frequency
sns.barplot(
    data=df,
    x="vehicle_type",
    y="delay_minutes",
    ax=axes[0, 1],
    palette="magma",
    errorbar=None,
)
axes[0, 1].set_title("2. Average Delay Severity by Courier Vehicle Type")
axes[0, 1].set_xlabel("Vehicle Type")
axes[0, 1].set_ylabel("Mean Delay (Minutes)")

# Panel 3: Delay vs Distance by Vehicle Type
sns.scatterplot(
    data=df,
    x="distance_km",
    y="delay_minutes",
    hue="vehicle_type",
    ax=axes[1, 0],
    alpha=0.6,
)
axes[1, 0].axhline(0, color="red", linestyle="--")
axes[1, 0].set_title("3. Bicycles Fail On Longer Distances (>3 km)")
axes[1, 0].set_xlabel("Distance (km)")
axes[1, 0].set_ylabel("Delay (Minutes)")

# Panel 4: Delay by Hour of Day
hourly_delay = (
    df.groupby("order_hour")["delay_minutes"].mean().reset_index()
)
sns.lineplot(
    data=hourly_delay,
    x="order_hour",
    y="delay_minutes",
    ax=axes[1, 1],
    marker="o",
    color="crimson",
)
axes[1, 1].set_title("4. Average Delay Spikes During Peak Hours (18:00 - 22:00)")
axes[1, 1].set_xlabel("Hour of Day")
axes[1, 1].set_ylabel("Mean Delay (Minutes)")

# Panel 5: Prep Time Bottleneck by Cuisine/Restaurant
top_prep = (
    df.groupby("cuisine")["prep_minutes"].mean().sort_values(ascending=False).reset_index()
)
sns.barplot(
    data=top_prep,
    x="prep_minutes",
    y="cuisine",
    ax=axes[2, 0],
    palette="viridis",
)
axes[2, 0].set_title("5. Kitchen Prep Time Bottlenecks by Cuisine")
axes[2, 0].set_xlabel("Mean Prep Time (Minutes)")
axes[2, 0].set_ylabel("Cuisine")

# Panel 6: Missing Rating Analysis
df["has_rating"] = df["customer_rating"].notnull().astype(str)
sns.boxplot(
    data=df,
    x="has_rating",
    y="delay_minutes",
    ax=axes[2, 1],
    palette="Set2",
)
axes[2, 1].set_title("6. Unrated Orders Suffer Higher Delays Than Rated Orders")
axes[2, 1].set_xlabel("Customer Left a Rating? (True/False)")
axes[2, 1].set_ylabel("Delay (Minutes)")

plt.tight_layout()
plt.savefig("sahl_dashboard.png", dpi=300)
plt.close()