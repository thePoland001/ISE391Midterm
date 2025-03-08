import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("exam_1_data.csv")

def get_location(sensor_id):
    if 1 <= sensor_id <= 12:
        return "HA"
    elif 13 <= sensor_id <= 24:
        return "FA"
    elif 25 <= sensor_id <= 36:
        return "UA"

df["location"] = df["sensor"].apply(get_location)

df.head()

grouped_loc_gap = df.groupby(["location", "gap_duration"])["error"]

mean_error_loc_gap = grouped_loc_gap.mean().reset_index(name="mean_error")
std_error_loc_gap = grouped_loc_gap.std().reset_index(name="std_error")

stats_loc_gap = pd.merge(mean_error_loc_gap, std_error_loc_gap, on=["location", "gap_duration"])
stats_loc_gap.head()

locations = ["HA", "FA", "UA"]

for loc in locations:
    df_loc = stats_loc_gap[stats_loc_gap["location"] == loc]

    plt.figure()
    plt.scatter(df_loc["gap_duration"], df_loc["mean_error"])
    plt.title(f"{loc}: Gap Duration vs. Mean Error")
    plt.xlabel("Gap Duration (minutes)")
    plt.ylabel("Error (degrees)")
    plt.show()

for loc in locations:
    df_loc = stats_loc_gap[stats_loc_gap["location"] == loc]

    x = df_loc["gap_duration"]
    y = df_loc["mean_error"]

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    r_squared = r_value**2

    print(f"\nLocation: {loc}")
    print(f"  Slope = {slope:.4f}")
    print(f"  Intercept = {intercept:.4f}")
    print(f"  r = {r_value:.4f}")
    print(f"  r^2 = {r_squared:.4f}")
    print(f"  p-value (for slope) = {p_value:.4e}")
    print(f"  Std error (of slope) = {std_err:.4f}")

for loc in locations:
    df_loc = df[df["location"] == loc]

    plt.figure()
    plt.scatter(df_loc["gap_duration"], df_loc["error"])
    plt.title(f"{loc}: Gap Duration vs. Error (all individuals)")
    plt.xlabel("Gap Duration (minutes)")
    plt.ylabel("Error (degrees)")
    plt.show()

for loc in locations:
    df_loc = df[df["location"] == loc]
    x = df_loc["gap_duration"]
    y = df_loc["error"]

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    r_squared = r_value**2

    print(f"\nLocation: {loc} (Raw Data)")
    print(f"  Slope = {slope:.4f}")
    print(f"  Intercept = {intercept:.4f}")
    print(f"  r = {r_value:.4f}")
    print(f"  r^2 = {r_squared:.4f}")
    print(f"  p-value (for slope) = {p_value:.4e}")
    print(f"  Std error (of slope) = {std_err:.4f}")
