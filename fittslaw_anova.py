"""Fitts' Law two-way ANOVA analysis (headless container version).

Encapsulates the Fitts' Law analysis pipeline in ``FittsLawAnalysis``.
Figures are written to ``figures/`` instead of being shown interactively
because this module runs inside a headless Docker container.
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


class FittsLawAnalysis:
    """Two-way ANOVA pipeline for Fitts' Law experiment results.

    Loads a merged CSV of per-trial summaries and exposes plotting and
    statistical-test methods. Results are printed to stdout and figures
    are saved under ``figure_dir``.
    """

    column_rename_map = {
        "Participant Code": "participant_code",
        "Session Code": "session_code",
        "Condition Code": "condition_code",
        "Hand Dominance": "hand_dominance",
        "Mean Completion Time (ms)": "mean_completion_time",
        "Mean Click Error (%)": "mean_click_error",
        "Mean Throughput (bps)": "mean_throughput",
    }
    hand_order = ["Dominant", "Non-Dominant"]
    session_order = ["S0", "S1", "S2", "S3", "S4"]
    alpha = 0.05

    def __init__(self, csv_path, figure_dir="figures"):
        """Load the CSV and prepare the output figure directory.

        Args:
            csv_path: Absolute path to the merged Fitts' Law CSV.
            figure_dir: Directory where PNG figures will be written.
        """
        self.csv_path = csv_path
        self.figure_dir = figure_dir
        os.makedirs(self.figure_dir, exist_ok=True)
        self.df = self._load_data()

    def _load_data(self):
        """Read the CSV and rename columns to snake_case identifiers."""
        df = pd.read_csv(self.csv_path)
        return df.rename(columns=self.column_rename_map)

    def _save_figure(self, fig, filename):
        """Save ``fig`` under ``figure_dir`` and release its memory."""
        path = os.path.join(self.figure_dir, filename)
        fig.savefig(path, bbox_inches="tight", dpi=120)
        plt.close(fig)
        print(f"Saved figure: {path}")

    def print_summary(self):
        """Print the head and per-participant row counts of the dataset."""
        print("--- Data Head ---")
        print(self.df.head())
        print()

        print(f"--- Record Count: {len(self.df)} rows ---")
        print("Rows per participant:")
        print(self.df["participant_code"].value_counts().sort_index())
        print()

    def plot_hand_dominance(self):
        """Save bar plots of completion time and click error by hand."""
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        sns.barplot(
            ax=axes[0],
            data=self.df,
            x="hand_dominance",
            y="mean_completion_time",
            ci="sd",
            capsize=0.05,
            order=self.hand_order,
            palette="Greens",
        )
        axes[0].set_xlabel("Hand Dominance")
        axes[0].set_ylabel("Mean Completion Time (ms)")

        axes[1].set_ylim(bottom=0, top=20)
        sns.barplot(
            ax=axes[1],
            data=self.df,
            x="hand_dominance",
            y="mean_click_error",
            ci="sd",
            capsize=0.05,
            order=self.hand_order,
            palette="Greens",
        )
        axes[1].set_xlabel("Hand Dominance")
        axes[1].set_ylabel("Mean Click Error (%)")
        self._save_figure(fig, "01_hand_dominance.png")

    def plot_sessions(self):
        """Save bar plots of completion time and click error by session."""
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        sns.barplot(
            ax=axes[0],
            data=self.df,
            x="session_code",
            y="mean_completion_time",
            ci="sd",
            capsize=0.15,
            order=self.session_order,
            palette="Blues",
        )
        axes[0].set_xlabel("Session Code")
        axes[0].set_ylabel("Mean Completion Time (ms)")

        axes[1].set_ylim(bottom=0, top=100)
        sns.barplot(
            ax=axes[1],
            data=self.df,
            x="session_code",
            y="mean_click_error",
            ci="sd",
            capsize=0.15,
            order=self.session_order,
            palette="Blues",
        )
        axes[1].set_xlabel("Session Code")
        axes[1].set_ylabel("Mean Click Error (%)")
        self._save_figure(fig, "02_session_code.png")

    def run_anova_completion_time(self):
        """Run two-way ANOVA on completion time and assumption checks.

        Prints the ANOVA table, Shapiro-Wilk normality test, Levene's
        test of equal variance across hands, and Mauchly's sphericity
        test across sessions. Saves a Q-Q plot of the residuals.
        """
        print("=== Two-Way ANOVA: Mean Completion Time ===")
        time_model = ols(
            "mean_completion_time ~ C(hand_dominance) + C(session_code)"
            " + C(hand_dominance):C(session_code)",
            data=self.df,
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
        if shapiro_test.pvalue > self.alpha:
            print("Result: Fail to reject H0. Residuals appear normal.\n")
        else:
            print("Result: Reject H0. Residuals not normal.\n")

        fig = plt.figure(figsize=(6, 6))
        sm.qqplot(residuals, line="s", ax=plt.gca())
        plt.title("Normal Q-Q Plot (Residuals)")
        self._save_figure(fig, "03_qqplot_completion_time.png")

        dominant = self.df[self.df["hand_dominance"] == "Dominant"]
        non_dominant = self.df[self.df["hand_dominance"] == "Non-Dominant"]
        levene_hand = stats.levene(
            dominant["mean_completion_time"],
            non_dominant["mean_completion_time"],
        )
        print("--- Levene's Test (Hand Dominance) ---")
        print(
            f"Statistic: {levene_hand.statistic:.4f}, "
            f"p-value: {levene_hand.pvalue:.4f}"
        )
        if levene_hand.pvalue > self.alpha:
            print("Result: Variances are equal.\n")
        else:
            print("Result: Variances are unequal.\n")

        spher_test = pg.sphericity(
            data=self.df,
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

    def run_tukey_completion_time(self):
        """Run Tukey HSD on completion time for hand, session, and pair."""
        print("=== Tukey HSD: Mean Completion Time ===")
        self._print_tukey_triplet("mean_completion_time")

    def run_anova_click_error(self):
        """Run two-way ANOVA on click error and print the table."""
        print("=== Two-Way ANOVA: Mean Click Error ===")
        error_model = ols(
            "mean_click_error ~ C(hand_dominance) + C(session_code)"
            " + C(hand_dominance):C(session_code)",
            data=self.df,
        ).fit()
        print(sm.stats.anova_lm(error_model, typ=2))
        print()

    def run_tukey_click_error(self):
        """Run Tukey HSD on click error for hand, session, and pair."""
        print("=== Tukey HSD: Mean Click Error ===")
        self._print_tukey_triplet("mean_click_error")

    def _print_tukey_triplet(self, metric):
        """Print Tukey HSD by hand, by session, and by hand+session."""
        tukey_hand = pairwise_tukeyhsd(
            endog=self.df[metric],
            groups=self.df["hand_dominance"],
            alpha=self.alpha,
        )
        tukey_session = pairwise_tukeyhsd(
            endog=self.df[metric],
            groups=self.df["session_code"],
            alpha=self.alpha,
        )
        tukey_hand_session = pairwise_tukeyhsd(
            endog=self.df[metric],
            groups=self.df["hand_dominance"] + self.df["session_code"],
            alpha=self.alpha,
        )
        print(tukey_hand)
        print()
        print(tukey_session)
        print()
        print(tukey_hand_session)
        print()

    def run_all(self):
        """Execute the full pipeline matching the original script."""
        self.print_summary()
        self.plot_hand_dominance()
        self.plot_sessions()
        self.run_anova_completion_time()
        self.run_tukey_completion_time()
        self.run_anova_click_error()
        self.run_tukey_click_error()


if __name__ == "__main__":
    csv_path = "/workspace/sungwoo_docker/Anova/Data/overall_merged.csv"
    analysis = FittsLawAnalysis(csv_path)
    analysis.run_all()
