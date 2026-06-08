# -*- coding: utf-8 -*-
"""
두 집단(A/B) 만족도(리커트 7점) 가상 데이터 독립표본 t-검정
- Levene 등분산 검정, Cohen's d 효과크기, 95% 신뢰구간 포함
"""
import numpy as np
import pandas as pd
from scipy import stats

# ─────────────────────────────────────────────
# 1. 가상 데이터 생성 (N=200, 두 집단 A/B, 리커트 7점)
# ─────────────────────────────────────────────
rng = np.random.default_rng(42)  # 재현성 확보
n_per = 100

# 집단별 모평균을 다르게 설정해 차이가 존재하도록 생성
a_raw = rng.normal(loc=4.5, scale=1.2, size=n_per)
b_raw = rng.normal(loc=5.2, scale=1.1, size=n_per)

# 리커트 7점 척도로 변환: 1~7 정수로 반올림·절단(clip)
def to_likert(x):
    return np.clip(np.round(x), 1, 7).astype(int)

df = pd.DataFrame({
    "id": np.arange(1, 2 * n_per + 1),
    "group": ["A"] * n_per + ["B"] * n_per,
    "satisfaction": np.concatenate([to_likert(a_raw), to_likert(b_raw)]),
})

print("=" * 55)
print("[1] 데이터 미리보기 / 기술통계")
print("=" * 55)
print(df.head())
print()
desc = df.groupby("group")["satisfaction"].agg(["count", "mean", "std"]).round(3)
print(desc)
print()

a = df.loc[df.group == "A", "satisfaction"].to_numpy()
b = df.loc[df.group == "B", "satisfaction"].to_numpy()
n1, n2 = len(a), len(b)
m1, m2 = a.mean(), b.mean()
s1, s2 = a.std(ddof=1), b.std(ddof=1)

# ─────────────────────────────────────────────
# 2~3. Levene 등분산 검정
# ─────────────────────────────────────────────
lev_stat, lev_p = stats.levene(a, b, center="mean")
equal_var = lev_p > 0.05
print("=" * 55)
print("[2] Levene 등분산 검정")
print("=" * 55)
print(f"  W = {lev_stat:.3f}, p = {lev_p:.3f}  ->  "
      f"{'등분산 가정 충족' if equal_var else '등분산 가정 위배(Welch 사용)'}")
print()

# ─────────────────────────────────────────────
# 독립표본 t-검정 (등분산 여부에 따라 Student/Welch)
# ─────────────────────────────────────────────
t_stat, p_val = stats.ttest_ind(a, b, equal_var=equal_var)

# 자유도
if equal_var:
    dfree = n1 + n2 - 2
else:  # Welch-Satterthwaite
    dfree = ((s1**2/n1 + s2**2/n2)**2 /
             ((s1**2/n1)**2/(n1-1) + (s2**2/n2)**2/(n2-1)))

print("=" * 55)
print("[3] 독립표본 t-검정")
print("=" * 55)
print(f"  t({dfree:.1f}) = {t_stat:.3f}, p = {p_val:.4f}")
print()

# ─────────────────────────────────────────────
# Cohen's d (pooled SD 기준) + 효과크기 해석
# ─────────────────────────────────────────────
pooled_sd = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))
cohen_d = (m1 - m2) / pooled_sd

def interpret_d(d):
    ad = abs(d)
    if ad < 0.2:  return "무시할 수준"
    if ad < 0.5:  return "작은 효과"
    if ad < 0.8:  return "중간 효과"
    return "큰 효과"

# ─────────────────────────────────────────────
# 평균차의 95% 신뢰구간
# ─────────────────────────────────────────────
mean_diff = m1 - m2
if equal_var:
    se = pooled_sd * np.sqrt(1/n1 + 1/n2)
else:
    se = np.sqrt(s1**2/n1 + s2**2/n2)
t_crit = stats.t.ppf(0.975, dfree)
ci_low, ci_high = mean_diff - t_crit*se, mean_diff + t_crit*se

print("=" * 55)
print("[4] 효과크기 / 신뢰구간")
print("=" * 55)
print(f"  Cohen's d = {cohen_d:.3f} ({interpret_d(cohen_d)})")
print(f"  평균차(A-B) = {mean_diff:.3f}")
print(f"  95% CI = [{ci_low:.3f}, {ci_high:.3f}]")
print()

# ─────────────────────────────────────────────
# 4. APA 양식 결과표 (마크다운)
# ─────────────────────────────────────────────
star = "***" if p_val < .001 else "**" if p_val < .01 else "*" if p_val < .05 else ""
p_disp = "< .001" if p_val < .001 else f"= {p_val:.3f}"

md = f"""
### Table 1
*집단 간 만족도 차이에 대한 독립표본 t-검정 결과*

| 집단 | *n* | *M* | *SD* | *t* | *df* | *p* | Cohen's *d* | 95% CI [LL, UL] |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| A | {n1} | {m1:.2f} | {s1:.2f} | {t_stat:.2f}{star} | {dfree:.1f} | {p_disp} | {cohen_d:.2f} | [{ci_low:.2f}, {ci_high:.2f}] |
| B | {n2} | {m2:.2f} | {s2:.2f} | | | | | |

*주.* 리커트 7점 척도(1=전혀 그렇지 않다 ~ 7=매우 그렇다). \
Levene 등분산 검정 *W* = {lev_stat:.2f}, *p* = {lev_p:.3f}. \
{'등분산 가정이 충족되어 Student t-검정' if equal_var else 'Welch t-검정'}을 사용함. \
95% CI는 평균차(A-B)에 대한 신뢰구간. \\* *p* < .05, \\*\\* *p* < .01, \\*\\*\\* *p* < .001.
"""
print(md)

with open("ttest_result_table.md", "w", encoding="utf-8") as f:
    f.write(md)
