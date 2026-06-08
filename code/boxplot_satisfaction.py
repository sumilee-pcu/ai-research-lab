# -*- coding: utf-8 -*-
"""집단별 만족도 Boxplot (seaborn) — 색맹 친화 팔레트, 한글 라벨, 300dpi PNG"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# ── 한글 폰트 등록 (맑은 고딕) ──
font_path = r"C:\Windows\Fonts\malgun.ttf"
fm.fontManager.addfont(font_path)
KFONT = fm.FontProperties(fname=font_path).get_name()

# ── 동일 데이터 재생성 (seed 42, 앞선 분석과 일치) ──
rng = np.random.default_rng(42)
n_per = 100
a_raw = rng.normal(4.5, 1.2, n_per)
b_raw = rng.normal(5.2, 1.1, n_per)
to_likert = lambda x: np.clip(np.round(x), 1, 7).astype(int)
df = pd.DataFrame({
    "group": ["A"] * n_per + ["B"] * n_per,
    "satisfaction": np.concatenate([to_likert(a_raw), to_likert(b_raw)]),
})

# ── 그리기 ──
sns.set_theme(style="whitegrid")
# set_theme()이 rcParams를 초기화하므로 폰트 설정은 반드시 그 뒤에!
plt.rcParams["font.family"] = KFONT
plt.rcParams["axes.unicode_minus"] = False  # 마이너스 깨짐 방지
palette = sns.color_palette("colorblind", 2)  # 색맹 친화 팔레트

fig, ax = plt.subplots(figsize=(7, 6))
sns.boxplot(data=df, x="group", y="satisfaction", hue="group",
            palette=palette, width=0.5, fliersize=4, legend=False, ax=ax)
# 개별 관측치를 반투명 점으로 중첩(분포 확인용)
sns.stripplot(data=df, x="group", y="satisfaction",
              color="0.25", size=3, alpha=0.35, jitter=0.18, ax=ax)

ax.set_title("집단별 만족도 분포 비교", fontsize=15, fontweight="bold", pad=14)
ax.set_xlabel("집단", fontsize=12)
ax.set_ylabel("만족도 (리커트 7점)", fontsize=12)
ax.set_xticks([0, 1])
ax.set_xticklabels(["A 집단", "B 집단"])
ax.set_ylim(0.5, 7.5)
ax.set_yticks(range(1, 8))

fig.tight_layout()
out = "boxplot_satisfaction.png"
fig.savefig(out, dpi=300, bbox_inches="tight")
print(f"saved: {out}")
print("group means:", df.groupby('group')['satisfaction'].mean().round(2).to_dict())
