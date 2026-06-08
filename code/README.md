# 재현 코드 — 제9장 바이브코딩 분석

> 책 제9장(바이브코딩 분석)과 제10장(논문 시각화)의 분석·그래프를 그대로 돌려 볼 수 있는 Python 예제입니다.
> 연결 프롬프트: [P-9 분석 코드](../prompts/P09_분석코드.md) · [P-10 시각화](../prompts/P10_시각화.md) · 워크북: [W-5](../workbook/W5_데이터수집과분석자동화.md)

## 무엇을 보여주나

"AI에게 분석 코드를 시키면 어디까지 맡기고 어디서 검증해야 하는가"를 실제 코드로 보여줍니다. 두 스크립트 모두 고정 시드(seed=42)로 가상 데이터를 생성하므로, 누가 실행해도 똑같은 결과가 나옵니다(재현성). 실제 연구에서는 이 가상 데이터 부분을 본인의 데이터 파일 로드로 바꾸면 됩니다.

| 파일 | 내용 | 책 연결 |
|---|---|---|
| [`ttest_analysis.py`](ttest_analysis.py) | 두 집단 만족도(리커트 7점) 독립표본 t-검정 — Levene 등분산 검정, Cohen's d 효과크기, 95% 신뢰구간, APA 양식 결과표 생성 | 9장 |
| [`boxplot_satisfaction.py`](boxplot_satisfaction.py) | 집단별 만족도 분포 박스플롯 — 색맹 친화 팔레트, 한글 라벨, 300dpi PNG 저장 | 10장 |

## 실행 방법

```bash
# 1) 가상환경 (선택)
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2) 패키지 설치
pip install -r requirements.txt

# 3) 분석 실행 → 콘솔에 결과 + ttest_result_table.md 생성
python ttest_analysis.py

# 4) 그래프 실행 → boxplot_satisfaction.png 생성 (300dpi)
python boxplot_satisfaction.py
```

> 한글 폰트 주의: `boxplot_satisfaction.py`는 Windows 기본 폰트(맑은 고딕, `C:\Windows\Fonts\malgun.ttf`)를 사용합니다. macOS/Linux에서는 `font_path`를 `AppleGothic`이나 `NanumGothic` 경로로 바꿔 주세요.

## 예상 결과 (seed=42)

```
Table 1. 집단 간 만족도 차이에 대한 독립표본 t-검정 결과
A: n=100, M=4.40, SD=1.01
B: n=100, M=5.16, SD=1.05
t(198) = -5.23, p < .001, Cohen's d = -0.74 (중간~큰 효과), 95% CI [-1.05, -0.47]
```

## ⚠️ 연구자 책임 (꼭 읽으세요)

AI가 만든 분석 코드는 문법은 맞아도 연구 설계상 틀릴 수 있습니다. 코드를 돌리기 전·후로 아래를 직접 확인하세요.

- [ ] 변수 매핑 — X/Y/통제변수가 내 데이터 컬럼과 실제로 일치하는가
- [ ] 결측치·이상치 — 처리 방침을 내가 정했는가 (코드가 임의로 버리지 않았는가)
- [ ] 통계 전제 — 정규성·등분산 등 가정 검정을 거쳤는가
- [ ] p값 과대해석 금지 — "유의하다"와 "효과가 크다"는 다른 말. 효과크기를 함께 보고
- [ ] 데이터를 보지 못한 AI는 수치를 지어낼 수 있다 — 실제 수치는 반드시 내 데이터로 재실행해 확인

자세한 코드 생성·검증 프롬프트는 [P-9](../prompts/P09_분석코드.md)를 참고하세요.

## 라이선스

이 디렉터리의 코드는 MIT License(저장소 [LICENSE](../LICENSE) 하단)를 따릅니다. 자유롭게 수정·재사용하세요.
