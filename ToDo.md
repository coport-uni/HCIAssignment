# ToDo

## 2026-04-14: Bootstrap CommonClaude conventions + init repo

- [x] Generate initial `CLAUDE.md` describing Fitts' Law ANOVA notebook
- [x] Replace `CLAUDE.md` with CommonClaude (coport-uni/CommonClaude) version
- [x] Install `.claude/settings.json` and hooks (`pre-write-guard.sh`, `post-write-lint.sh`, `post-write-debug-remind.sh`)
- [x] Install `ruff.toml` (80-column limit)
- [x] `git init` and create `main` branch
- [x] Create public GitHub repo `HCIAssignment` and push
- [x] Open GitHub issue for this task via `gh issue create` (#1)

## 2026-04-14: Convert notebook to Python script (issue #2)

- [x] Convert `Fittslaw_Graph_2ANOVA-python.ipynb` to `fittslaw_anova.py`
- [x] Use Agg matplotlib backend (headless container)
- [x] Replace `plt.show()` with `savefig` to `figures/`
- [x] Pass ruff lint and format checks
- [x] Run script end-to-end; verify ANOVA output and 3 PNG figures

## 2026-04-14: Session code S0-S4 + anova conda env (issue #3)

- [x] Update barplot `order` from `S1-S5` to `S0-S4` in `fittslaw_anova.py`
- [x] Create conda env `anova` (python 3.11)
- [x] Install pandas, seaborn, matplotlib, statsmodels, scipy, pingouin
- [x] Verify `conda run -n anova python fittslaw_anova.py` executes successfully

## 2026-04-14: Write README with concepts (issue #4)

- [x] Draft README.md with project overview and usage
- [x] Add beginner-friendly Fitts' Law explanation
- [x] Add two-way ANOVA / Tukey HSD / assumption-check explanation
- [x] Document input CSV schema and output figures

## 2026-04-14: Print record count (issue #5)

- [x] Add `len(df)` print + groupby breakdown after data load
- [x] Verify script reports 80 rows

## 2026-04-14: Refactor fittslaw_anova.py into FittsLawAnalysis class

- [x] Define `FittsLawAnalysis` class in `fittslaw_anova.py`
- [x] Move CSV loading + column rename into `_load_data()`
- [x] Add `print_summary()` for record counts per participant
- [x] Add `plot_hand_dominance()` and `plot_sessions()` methods
- [x] Add `run_anova_completion_time()` and `run_tukey_completion_time()`
- [x] Add `run_anova_click_error()` and `run_tukey_click_error()`
- [x] Add `_save_figure()` staticmethod helper
- [x] Add `if __name__ == "__main__":` entry point preserving output
- [x] Verify MIT naming (verbs for methods, nouns for variables)
- [x] Verify 80-column limit
- [x] Pass `ruff check` and `ruff format --check`
- [x] Open GitHub issue via `gh issue create`
- [x] Commit and push

## 2026-04-14: Rewrite README.md in English

- [x] Translate all sections of README.md to English
- [x] Preserve section structure, tables, and math notation
- [x] Open GitHub issue via `gh issue create`
- [x] Commit and push
