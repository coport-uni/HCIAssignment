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
