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
