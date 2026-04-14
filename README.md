# HCIAssignment — Fitts' Law Two-Way ANOVA

Fitts' Law 실험 데이터에 대해 두-요인 분산분석(Two-Way ANOVA)과 사후검정
(Tukey HSD), 그리고 각종 통계 가정 검정을 수행하는 프로젝트입니다.

---

## 1. 배경 개념

### 1.1 Fitts' Law (피츠의 법칙)

Fitts' Law는 **목표 지점까지 손(또는 커서)을 움직이는 데 걸리는 시간**을
설명하는 HCI(Human-Computer Interaction)의 고전적 모델입니다 (Fitts, 1954).

핵심 아이디어는 간단합니다.

- 목표가 **멀수록**, **작을수록** 도달하는 데 시간이 더 걸린다.
- 이 관계를 정량화한 식:

  $$ MT = a + b \cdot \log_2\!\left(\frac{D}{W} + 1\right) $$

  - `MT` : Movement Time (완료 시간)
  - `D`  : 시작점에서 목표까지의 거리
  - `W`  : 목표의 너비
  - `log2(D/W + 1)` 부분을 **ID (Index of Difficulty)** 라고 부르며, 난이도가
    높을수록 값이 커집니다.
  - 이 식을 뒤집어 `Throughput (bps) = ID / MT` 로 정의하면 **초당 정보 처리량**
    을 얻을 수 있으며, 입력 장치(마우스, 터치패드 등)의 성능 지표로 쓰입니다.

본 실험에서는 참가자가 화면의 원형 타겟을 반복 클릭하면서 아래 지표를
기록했습니다.

| 지표 | 의미 |
|------|------|
| `mean_completion_time` (ms) | 타겟 한 개 클릭 평균 시간 |
| `mean_click_error` (%)      | 빗나간 클릭 비율 |
| `mean_throughput` (bps)     | 초당 처리 정보량 |

### 1.2 ANOVA (분산분석)

ANOVA는 **여러 그룹의 평균이 서로 다른가?** 를 판정하는 통계 기법입니다.
t-검정은 두 그룹만 비교할 수 있지만, ANOVA는 3개 이상의 그룹도 한 번에
비교할 수 있고, **두 개 이상의 요인**도 동시에 다룰 수 있습니다.

- **One-Way ANOVA**: 요인 1개 (예: 세션만)
- **Two-Way ANOVA**: 요인 2개 (예: 세션 × 주손 여부)
  - **주효과 (main effect)**: 각 요인이 독립적으로 결과에 미치는 영향
  - **상호작용 (interaction)**: 한 요인의 효과가 다른 요인의 수준에 따라
    달라지는지 여부

해석은 **p-value** 로 합니다. 관례적으로 `p < 0.05` 이면 "그 요인은 유의한
영향을 준다"라고 결론 짓습니다.

본 실험의 두 요인:

- `hand_dominance` : `Dominant` / `Non-Dominant`
- `session_code`   : `S0, S1, S2, S3, S4` (반복 학습 세션)

### 1.3 Tukey HSD (사후검정)

ANOVA는 "그룹 간에 차이가 있다/없다"만 알려줄 뿐, **어느 그룹 쌍이 다른지**
는 말해주지 않습니다. Tukey HSD는 가능한 모든 쌍을 비교하면서 다중 비교로
인한 오탐(Type I error)을 보정해 줍니다. 결과 테이블의 `reject=True` 는
해당 그룹 쌍이 유의하게 다르다는 뜻입니다.

### 1.4 ANOVA의 가정 검정

ANOVA 결과가 신뢰되려면 다음 가정이 만족되어야 합니다. 본 스크립트는 이를
자동으로 검사합니다.

| 가정 | 검정 방법 | 통과 조건 |
|------|-----------|-----------|
| 잔차의 정규성 | Shapiro-Wilk, Q-Q plot | `p > 0.05` |
| 분산의 동질성 (등분산성) | Levene's test | `p > 0.05` |
| 구형성 (반복측정 간 분산 동일) | Mauchly's test | `p > 0.05` |

가정이 깨지면 비모수 검정(Kruskal-Wallis 등)이나 Greenhouse-Geisser 보정을
고려해야 합니다.

---

## 2. 저장소 구성

```
Anova/
├── fittslaw_anova.py                   # 메인 분석 스크립트
├── Fittslaw_Graph_2ANOVA-python.ipynb  # 원본 Jupyter 노트북
├── Data/
│   └── overall_merged.csv              # 병합된 실험 데이터
├── figures/                            # 실행 시 PNG 자동 생성
├── CLAUDE.md                           # Claude Code 세션 규약 (CommonClaude)
├── ToDo.md                             # 작업 이력
├── ruff.toml                           # 린터 설정 (80-col)
└── .claude/                            # 훅과 설정
    ├── settings.json
    └── hooks/
```

---

## 3. 환경 설정

컨테이너(Ubuntu 24.04) + conda 환경을 가정합니다.

```bash
conda create -n anova python=3.11 -y
conda activate anova
pip install pandas seaborn matplotlib statsmodels scipy pingouin
```

### 입력 데이터 스키마

`Data/overall_merged.csv` 는 아래 열을 가져야 합니다(스크립트가 내부적으로
snake_case 로 리네임합니다).

```
Filename, Participant Code, Session Code, Condition Code, Hand Dominance,
Pointing Device, Device Experience,
Mean Completion Time (ms), Mean Click Error (%), Mean Throughput (bps)
```

- `Session Code` : `S0`, `S1`, `S2`, `S3`, `S4`
- `Hand Dominance` : `Dominant`, `Non-Dominant`

---

## 4. 실행

```bash
conda activate anova
python fittslaw_anova.py
```

### 출력

1. **표준 출력 (터미널)**
   - 데이터 head
   - 두-요인 ANOVA 표 (완료 시간, 클릭 오류율)
   - Shapiro-Wilk, Levene, Mauchly 가정 검정 결과
   - Tukey HSD 쌍별 비교표 (주손, 세션, 상호작용)

2. **figures/ 폴더에 생성되는 그래프 (headless, `matplotlib Agg` 백엔드)**

   | 파일 | 내용 |
   |------|------|
   | `01_hand_dominance.png` | 주손 여부별 완료 시간 · 클릭 오류율 |
   | `02_session_code.png`   | 세션별 완료 시간 · 클릭 오류율 |
   | `03_qqplot_completion_time.png` | 잔차 정규성 Q-Q plot |

---

## 5. 결과 해석 가이드

- **ANOVA 표** 에서 관심 있는 행의 `PR(>F)` 값을 봅니다.
  - `< 0.05` 이면 해당 요인(또는 상호작용)이 유의한 영향을 줍니다.
- **Tukey HSD** 표의 `reject` 열이 `True` 인 행이 실제로 평균이 다른 그룹
  쌍입니다.
- **가정 검정** 결과가 모두 통과(`p > 0.05`)해야 위의 p-value 를 그대로
  신뢰할 수 있습니다. 깨진 항목이 있으면 대체 검정을 고려하세요.

---

## 6. 참고 자료

- Fitts, P. M. (1954). *The information capacity of the human motor system
  in controlling the amplitude of movement.* Journal of Experimental
  Psychology, 47(6), 381-391.
- MacKenzie, I. S. (1992). *Fitts' law as a research and design tool in
  human-computer interaction.* Human-Computer Interaction, 7(1), 91-139.
- `statsmodels`, `pingouin` 공식 문서
