"""Fitts' Law two-way ANOVA analysis (headless container version).

Converted from Fittslaw_Graph_2ANOVA-python.ipynb. Figures are saved
under ``figures/`` instead of being shown interactively.
"""

import os
import warnings

import matplotlib

matplotlib.use("Agg")

import pandas as pd
import pingouin as pg
import seaborn as sns
import statsmodels.api as sm
from matplotlib import pyplot as plt
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

warnings.filterwarnings("ignore")
sns.set(style="whitegrid", font_scale=1.2)

figure_dir = "figures"
os.makedirs(figure_dir, exist_ok=True)


def save_figure(fig, filename):
    """Save a figure to ``figures/`` and close it to free memory."""
    path = os.path.join(figure_dir, filename)
    fig.savefig(path, bbox_inches="tight", dpi=120)
    plt.close(fig)
    print(f"Saved figure: {path}")


# Loading the data
filename = "/workspace/sungwoo_docker/Anova/Data/overall_merged.csv"
df = pd.read_csv(filename)

df = df.rename(
    columns={
        "Participant Code": "participant_code",
        "Session Code": "session_code",
        "Condition Code": "condition_code",
        "Hand Dominance": "hand_dominance",
        "Mean Completion Time (ms)": "mean_completion_time",
        "Mean Click Error (%)": "mean_click_error",
        "Mean Throughput (bps)": "mean_throughput",
    }
)

print("--- Data Head ---")
print(df.head())
print()


# Visualizing the effect of hand dominance
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
sns.barplot(
    ax=axes[0],
    data=df,
    x="hand_dominance",
    y="mean_completion_time",
    ci="sd",
    capsize=0.05,
    order=["Dominant", "Non-Dominant"],
    palette="Greens",
)
axes[0].set_xlabel("Hand Dominance")
axes[0].set_ylabel("Mean Completion Time (ms)")

axes[1].set_ylim(bottom=0, top=20)
sns.barplot(
    ax=axes[1],
    data=df,
    x="hand_dominance",
    y="mean_click_error",
    ci="sd",
    capsize=0.05,
    order=["Dominant", "Non-Dominant"],
    palette="Greens",
)
axes[1].set_xlabel("Hand Dominance")
axes[1].set_ylabel("Mean Click Error (%)")
save_figure(fig, "01_hand_dominance.png")


# Visualizing the effect of sessions
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
sns.barplot(
    ax=axes[0],
    data=df,
    x="session_code",
    y="mean_completion_time",
    ci="sd",
    capsize=0.15,
    order=["S0", "S1", "S2", "S3", "S4"],
    palette="Blues",
)
axes[0].set_xlabel("Session Code")
axes[0].set_ylabel("Mean Completion Time (ms)")

axes[1].set_ylim(bottom=0, top=100)
sns.barplot(
    ax=axes[1],
    data=df,
    x="session_code",
    y="mean_click_error",
    ci="sd",
    capsize=0.15,
    order=["S0", "S1", "S2", "S3", "S4"],
    palette="Blues",
)
axes[1].set_xlabel("Session Code")
axes[1].set_ylabel("Mean Click Error (%)")
save_figure(fig, "02_session_code.png")


# Two-way ANOVA on mean completion time
print("=== Two-Way ANOVA: Mean Completion Time ===")
time_model = ols(
    "mean_completion_time ~ C(hand_dominance) + C(session_code)"
    " + C(hand_dominance):C(session_code)",
    data=df,
).fit()
print(sm.stats.anova_lm(time_model, typ=2))
print()

residuals = time_model.resid
shapiro_test = stats.shapiro(residuals)
print("--- Normality Check (Shapiro-Wilk) ---")
print(
    f"Statistic: {shapiro_test.statistic:.4f}, "
    f"p-value: {shapiro_test.pvalue:.4f}"
)
if shapiro_test.pvalue > 0.05:
    print("Result: Fail to reject H0. Residuals appear normal.\n")
else:
    print("Result: Reject H0. Residuals not normal.\n")

fig = plt.figure(figsize=(6, 6))
sm.qqplot(residuals, line="s", ax=plt.gca())
plt.title("Normal Q-Q Plot (Residuals)")
save_figure(fig, "03_qqplot_completion_time.png")

levene_hand = stats.levene(
    df[df["hand_dominance"] == "Dominant"]["mean_completion_time"],
    df[df["hand_dominance"] == "Non-Dominant"]["mean_completion_time"],
)
print("--- Levene's Test (Hand Dominance) ---")
print(
    f"Statistic: {levene_hand.statistic:.4f}, p-value: {levene_hand.pvalue:.4f}"
)
if levene_hand.pvalue > 0.05:
    print("Result: Variances are equal.\n")
else:
    print("Result: Variances are unequal.\n")

spher_test = pg.sphericity(
    data=df,
    dv="mean_completion_time",
    within="session_code",
    subject="participant_code",
)
print("--- Mauchly's Test of Sphericity ---")
print(f"W: {spher_test[1]:.4f}, p-value: {spher_test[4]:.4f}")
if spher_test[0]:
    print("Result: Sphericity met.\n")
else:
    print("Result: Sphericity violated.\n")


# Tukey HSD on mean completion time
print("=== Tukey HSD: Mean Completion Time ===")
tukey_hand = pairwise_tukeyhsd(
    endog=df["mean_completion_time"],
    groups=df["hand_dominance"],
    alpha=0.05,
)
tukey_session = pairwise_tukeyhsd(
    endog=df["mean_completion_time"],
    groups=df["session_code"],
    alpha=0.05,
)
tukey_hand_session = pairwise_tukeyhsd(
    endog=df["mean_completion_time"],
    groups=df["hand_dominance"] + df["session_code"],
    alpha=0.05,
)
print(tukey_hand)
print()
print(tukey_session)
print()
print(tukey_hand_session)
print()


# Two-way ANOVA on mean click error
print("=== Two-Way ANOVA: Mean Click Error ===")
error_model = ols(
    "mean_click_error ~ C(hand_dominance) + C(session_code)"
    " + C(hand_dominance):C(session_code)",
    data=df,
).fit()
print(sm.stats.anova_lm(error_model, typ=2))
print()


# Tukey HSD on mean click error
print("=== Tukey HSD: Mean Click Error ===")
tukey_hand = pairwise_tukeyhsd(
    endog=df["mean_click_error"],
    groups=df["hand_dominance"],
    alpha=0.05,
)
tukey_session = pairwise_tukeyhsd(
    endog=df["mean_click_error"],
    groups=df["session_code"],
    alpha=0.05,
)
tukey_hand_session = pairwise_tukeyhsd(
    endog=df["mean_click_error"],
    groups=df["hand_dominance"] + df["session_code"],
    alpha=0.05,
)
print(tukey_hand)
print()
print(tukey_session)
print()
print(tukey_hand_session)
