# HCIAssignment — Fitts' Law Two-Way ANOVA

A project that runs a two-way ANOVA, Tukey HSD post-hoc tests, and the
associated statistical-assumption checks on Fitts' Law experiment data.

---

## 1. Background Concepts

### 1.1 Fitts' Law

Fitts' Law is a classic model in HCI (Human-Computer Interaction) that
describes **the time required to move a hand (or cursor) to a target**
(Fitts, 1954).

The core idea is simple:

- The **farther** and **smaller** the target is, the longer it takes to
  reach.
- The quantitative relationship is:

  $$ MT = a + b \cdot \log_2\!\left(\frac{D}{W} + 1\right) $$

  - `MT` : Movement Time (completion time)
  - `D`  : distance from the starting point to the target
  - `W`  : width of the target
  - `log2(D/W + 1)` is the **Index of Difficulty (ID)**; higher values
    mean a harder task.
  - Rearranging gives `Throughput (bps) = ID / MT`, the **information
    throughput per second**, which is used as a performance metric for
    input devices such as mice and touchpads.

In this experiment, participants repeatedly clicked circular targets on
a screen while the following metrics were recorded.

| Metric | Meaning |
|--------|---------|
| `mean_completion_time` (ms) | Average time to click one target |
| `mean_click_error` (%)      | Proportion of missed clicks |
| `mean_throughput` (bps)     | Information throughput per second |

### 1.2 ANOVA (Analysis of Variance)

ANOVA is a statistical technique that tests **whether the means of
several groups differ**. A t-test compares only two groups, whereas
ANOVA can compare three or more groups at once and can also handle
**two or more factors** simultaneously.

- **One-Way ANOVA**: a single factor (for example, session only).
- **Two-Way ANOVA**: two factors (for example, session × hand
  dominance).
  - **Main effect**: the independent influence of each factor on the
    outcome.
  - **Interaction**: whether the effect of one factor depends on the
    level of the other factor.

Interpretation is done through the **p-value**. By convention,
`p < 0.05` means "this factor has a significant effect."

The two factors in this experiment:

- `hand_dominance` : `Dominant` / `Non-Dominant`
- `session_code`   : `S0, S1, S2, S3, S4` (repeated learning sessions)

### 1.3 Tukey HSD (Post-Hoc Test)

ANOVA only tells you "there is / is no difference between the groups";
it does **not** tell you **which specific pair of groups differs**.
Tukey HSD compares every possible pair while correcting for the
Type I error inflation caused by multiple comparisons. In the result
table, `reject=True` means the pair is significantly different.

### 1.4 ANOVA Assumption Checks

ANOVA results are only trustworthy when the following assumptions hold.
This script checks them automatically.

| Assumption | Test | Passes when |
|------------|------|-------------|
| Normality of residuals | Shapiro-Wilk, Q-Q plot | `p > 0.05` |
| Homogeneity of variance | Levene's test | `p > 0.05` |
| Sphericity (equal variance across repeated measures) | Mauchly's test | `p > 0.05` |

If an assumption is violated, consider a nonparametric test
(Kruskal-Wallis, etc.) or a Greenhouse-Geisser correction.

---

## 2. Repository Layout

```
Anova/
├── fittslaw_anova.py                   # Main analysis script
├── Fittslaw_Graph_2ANOVA-python.ipynb  # Original Jupyter notebook
├── Data/
│   └── overall_merged.csv              # Merged experiment data
├── figures/                            # PNGs generated at runtime
├── CLAUDE.md                           # Claude Code session rules (CommonClaude)
├── ToDo.md                             # Task history
├── ruff.toml                           # Linter config (80-col)
└── .claude/                            # Hooks and settings
    ├── settings.json
    └── hooks/
```

---

## 3. Environment Setup

Assumes a container (Ubuntu 24.04) plus a conda environment.

```bash
conda create -n anova python=3.11 -y
conda activate anova
pip install pandas seaborn matplotlib statsmodels scipy pingouin
```

### Input Data Schema

`Data/overall_merged.csv` must have the following columns (the script
renames them internally to snake_case).

```
Filename, Participant Code, Session Code, Condition Code, Hand Dominance,
Pointing Device, Device Experience,
Mean Completion Time (ms), Mean Click Error (%), Mean Throughput (bps)
```

- `Session Code` : `S0`, `S1`, `S2`, `S3`, `S4`
- `Hand Dominance` : `Dominant`, `Non-Dominant`

---

## 4. Running

```bash
conda activate anova
python fittslaw_anova.py
```

### Output

1. **Standard output (terminal)**
   - Data head
   - Two-way ANOVA tables (completion time, click-error rate)
   - Shapiro-Wilk, Levene, and Mauchly assumption-check results
   - Tukey HSD pairwise-comparison tables (hand, session, interaction)

2. **Figures saved under `figures/` (headless, `matplotlib Agg` backend)**

   | File | Contents |
   |------|----------|
   | `01_hand_dominance.png` | Completion time and click error by hand dominance |
   | `02_session_code.png`   | Completion time and click error by session |
   | `03_qqplot_completion_time.png` | Q-Q plot for residual normality |

---

## 5. How to Read the Results

- In the **ANOVA table**, look at the `PR(>F)` column for the row of
  interest.
  - `< 0.05` means the factor (or interaction) has a significant
    effect.
- In the **Tukey HSD** table, rows with `reject=True` are the group
  pairs whose means actually differ.
- All **assumption checks** should pass (`p > 0.05`) before you can
  trust the p-values above at face value. If any check fails, consider
  an alternative test.

---

## 6. References

- Fitts, P. M. (1954). *The information capacity of the human motor
  system in controlling the amplitude of movement.* Journal of
  Experimental Psychology, 47(6), 381-391.
- MacKenzie, I. S. (1992). *Fitts' law as a research and design tool in
  human-computer interaction.* Human-Computer Interaction, 7(1),
  91-139.
- Official documentation for `statsmodels` and `pingouin`.
