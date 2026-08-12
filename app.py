import streamlit as st
import pandas as pd


# ============================================================
# 1. 페이지 설정
# ============================================================

st.set_page_config(
    page_title="서울시민 스트레스와 생활 특성 분석",
    page_icon="📊",
    layout="wide",
)

# ============================================================
# 2. 데이터 불러오기
# ============================================================
@st.cache_data
def load_data():

    happiness = pd.read_csv("data/processed/happiness_processed.csv")
    hobby = pd.read_csv("data/processed/hobby_processed.csv")
    stress = pd.read_csv("data/processed/stress_processed.csv")
    worry = pd.read_csv("data/processed/worry_processed.csv")

    return happiness, hobby, stress, worry

happiness, hobby, stress, worry = load_data()

# ============================================================
# 3. 기본 설정
# ============================================================
analysis_groups = [
    "성별",
    "연령별",
    "학력별",
    "소득별",
    "혼인상태별",
    "직업분류",
    "지역소분류"
]

worry_cols = [
    "경제문제",
    "건강",
    "자녀양육",
    "노후생활",
    "가족문제",
    "공부",
    "진로",
    "결혼",
    "자기개발",
    "이성우정",
    "신체외모",
    "인터넷커뮤니티",
    "학교폭력",
    "기타"
]

happiness_cols = [
    "건강상태",
    "재정상태",
    "친지친구관계",
    "가정생활",
    "사회생활"
]

hobby_cols = [
    "관광",
    "스포츠활동",
    "문화예술관람",
    "문화예술참여",
    "스포츠관람",
    "취미오락",
    "휴식",
    "사회기타활동",
]

# ============================================================
# 4. 스트레스 + 행복 데이터 결합
# ============================================================
stress_happiness = stress[["구분", "구분상세", "스트레스체감률"]].merge(
    happiness[["구분", "구분상세", "행복지수"]],
    on=["구분", "구분상세"],how="inner")

# ============================================================
# 5. 스트레스·행복 유형 생성
# ============================================================
type_results = []

for group_name in analysis_groups:

    group_data = stress_happiness[stress_happiness["구분"] == group_name].copy()

    if group_data.empty:
        continue

    stress_mean = group_data["스트레스체감률"].mean()
    happiness_mean = group_data["행복지수"].mean()

    group_data["스트레스수준"] = group_data["스트레스체감률"].apply(lambda x: "높음" if x >= stress_mean else "낮음")

    group_data["행복수준"] = group_data["행복지수"].apply(lambda x: "높음" if x >= happiness_mean else "낮음")

    group_data["스트레스행복유형"] = (
        "스트레스 "
        + group_data["스트레스수준"]
        + " + 행복 "
        + group_data["행복수준"]
    )

    type_results.append(group_data)


stress_happiness_type = pd.concat(type_results,ignore_index=True,)


# ============================================================
# 6. 제목
# ============================================================
st.title("📊 서울시민의 집단별 스트레스와 생활 특성")

st.write(
    """
    연령·학력·소득·자치구 등 집단별 스트레스 수준을 비교하고,
    고민·행복·여가생활에서 어떤 특징과 차이가 나타나는지
    살펴봅니다.
    """
)

# ============================================================
# 7. 사이드바 - 분석 기준 선택
# ============================================================
st.sidebar.header("분석 조건")

selected_group = st.sidebar.selectbox("분석 기준을 선택하세요",analysis_groups,)

# ============================================================
# 8. 선택한 분류의 스트레스 데이터
# ============================================================
group_stress = stress[stress["구분"] == selected_group][["구분상세", "스트레스체감률", "스트레스점수"]].copy()

group_stress = group_stress.sort_values("스트레스체감률",ascending=False,ignore_index=True,)

# ============================================================
# 9. 집단별 스트레스 수준
# ============================================================
st.header("1. 집단별 스트레스 수준")
st.caption(f"{selected_group} 집단의 스트레스체감률을 비교합니다.")

if not group_stress.empty:

    highest = group_stress.iloc[0]
    lowest = group_stress.iloc[-1]

    col1, col2, col3 = st.columns(3)

    col1.metric("스트레스가 가장 높은 집단",highest["구분상세"],f"{highest['스트레스체감률']:.1f}%",)

    col2.metric("스트레스가 가장 낮은 집단",lowest["구분상세"],f"{lowest['스트레스체감률']:.1f}%",)

    gap = (highest["스트레스체감률"] - lowest["스트레스체감률"]
    )

    col3.metric("집단 간 격차",f"{gap:.1f}%p",)

    st.bar_chart(group_stress.set_index("구분상세")["스트레스체감률"])

    with st.expander("데이터 보기"):
        st.dataframe(
            group_stress,
            use_container_width=True,
            hide_index=True,
        )

# ============================================================
# 10. 전체 분류별 스트레스 격차
# ============================================================
st.header("2. 어떤 기준에서 스트레스 격차가 클까?")

gap_results = []
for group_name in analysis_groups:

    data = stress[stress["구분"] == group_name][["구분상세", "스트레스체감률"]].copy()

    if data.empty:
        continue

    highest_row = data.loc[data["스트레스체감률"].idxmax()]

    lowest_row = data.loc[data["스트레스체감률"].idxmin()]

    gap = (highest_row["스트레스체감률"] - lowest_row["스트레스체감률"]
    )

    gap_results.append(
        {
            "구분": group_name,
            "최고집단": highest_row["구분상세"],
            "최고체감률": highest_row["스트레스체감률"],
            "최저집단": lowest_row["구분상세"],
            "최저체감률": lowest_row["스트레스체감률"],
            "격차": round(gap, 1),
        }
    )


stress_gap = pd.DataFrame(gap_results)

stress_gap = stress_gap.sort_values("격차",ascending=False,)

st.bar_chart(stress_gap.set_index("구분")["격차"])

with st.expander("분류별 격차 데이터 보기"):
    st.dataframe(
        stress_gap,
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# 11. 세부 집단 선택
# ============================================================
st.divider()

st.subheader("🔎 세부 집단 탐색")

detail_groups = group_stress["구분상세"].tolist()

selected_detail = st.selectbox(f"{selected_group} 중 살펴볼 집단",detail_groups,)

# ============================================================
# 12. 선택 집단 기본 정보
# ============================================================
selected_stress = group_stress[group_stress["구분상세"] == selected_detail]

if not selected_stress.empty:

    stress_rate = selected_stress.iloc[0][
        "스트레스체감률"
    ]

else:
    stress_rate = None

selected_happiness = happiness[
    (happiness["구분"] == selected_group)
    & (happiness["구분상세"] == selected_detail)
]

if not selected_happiness.empty:
    happiness_score = selected_happiness.iloc[0][
        "행복지수"
    ]
else:
    happiness_score = None

col1, col2 = st.columns(2)

if stress_rate is not None:
    col1.metric(
        "스트레스체감률",
        f"{stress_rate:.1f}%",
    )

if happiness_score is not None:
    col2.metric(
        "행복지수",
        f"{happiness_score:.2f}",
    )


# ============================================================
# 13. 고민 TOP 5
# ============================================================
st.header("3. 주요 고민")

selected_worry = worry[
    (worry["구분"] == selected_group)
    & (worry["구분상세"] == selected_detail)
]

if not selected_worry.empty:
    top5_worry = (
        selected_worry[worry_cols]
        .iloc[0]
        .dropna()
        .sort_values(ascending=False)
        .head(5)
    )

    st.subheader(
        f"{selected_detail}의 주요 고민 TOP 5"
    )

    st.bar_chart(top5_worry)

    worry_table = top5_worry.reset_index()
    worry_table.columns = ["고민", "비율"]

    st.dataframe(
        worry_table,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "※ 고민 데이터는 과거 자료이므로 "
        "현재 스트레스의 직접적인 원인으로 해석하지 않습니다."
    )

else:
    st.info(
        "선택한 집단과 일치하는 고민 데이터가 없습니다."
    )


# ============================================================
# 14. 스트레스와 행복 비교
# ============================================================
st.header("4. 스트레스가 높으면 행복도 낮을까?")

selected_compare = stress_happiness[stress_happiness["구분"] == selected_group].copy()

selected_compare = selected_compare.sort_values("스트레스체감률",ascending=False,)

if not selected_compare.empty:
    st.dataframe(
        selected_compare,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("스트레스체감률")

    st.bar_chart(
        selected_compare.set_index(
            "구분상세"
        )["스트레스체감률"]
    )

    st.subheader("행복지수")

    st.bar_chart(
        selected_compare.set_index(
            "구분상세"
        )["행복지수"]
    )

# ============================================================
# 15. 스트레스·행복 유형
# ============================================================
st.header("5. 스트레스와 행복을 함께 보면?")

selected_type = stress_happiness_type[
    stress_happiness_type["구분"]
    == selected_group
][
    [
        "구분상세",
        "스트레스체감률",
        "행복지수",
        "스트레스행복유형",
    ]
].copy()


if not selected_type.empty:

    st.dataframe(
        selected_type,
        use_container_width=True,
        hide_index=True,
    )

    type_count = (
        selected_type[
            "스트레스행복유형"
        ]
        .value_counts()
    )

    st.subheader("유형별 집단 수")

    st.bar_chart(type_count)


# 선택한 세부 집단의 유형
selected_type_detail = selected_type[
    selected_type["구분상세"] == selected_detail
]


if not selected_type_detail.empty:

    current_type = selected_type_detail.iloc[0][
        "스트레스행복유형"
    ]

    st.info(
        f"**{selected_detail}**은 "
        f"**{current_type}** 유형입니다."
    )


# ============================================================
# 16. 행복 세부 영역
# ============================================================
st.header("6. 행복의 어떤 영역에서 차이가 날까?")

selected_happiness_detail = happiness[
    (happiness["구분"] == selected_group)
    & (happiness["구분상세"] == selected_detail)
]

if not selected_happiness_detail.empty:

    happiness_detail = (
        selected_happiness_detail[
            happiness_cols
        ]
        .iloc[0]
        .dropna()
        .sort_values(ascending=False)
    )

    st.bar_chart(happiness_detail)

    highest_happiness_area = (
        happiness_detail.idxmax()
    )

    lowest_happiness_area = (
        happiness_detail.idxmin()
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "가장 높은 행복 영역",
        highest_happiness_area,
        f"{happiness_detail.max():.2f}",
    )

    col2.metric(
        "가장 낮은 행복 영역",
        lowest_happiness_area,
        f"{happiness_detail.min():.2f}",
    )

else:

    st.info(
        "선택한 집단의 행복 세부 데이터가 없습니다."
    )


# ============================================================
# 17. 여가생활
# ============================================================
st.header("7. 여가생활에는 어떤 특징이 있을까?")

selected_hobby = hobby[
    (hobby["구분"] == selected_group)
    & (hobby["구분상세"] == selected_detail)
]


if not selected_hobby.empty:
    hobby_detail = (
        selected_hobby[hobby_cols]
        .iloc[0]
        .dropna()
        .sort_values(ascending=False)
    )

    st.bar_chart(hobby_detail)

    hobby_table = hobby_detail.reset_index()
    hobby_table.columns = [
        "여가활동",
        "비율",
    ]

    st.dataframe(
        hobby_table,
        use_container_width=True,
        hide_index=True,
    )

else:
    st.info(
        "선택한 집단의 여가활동 데이터가 없습니다."
    )

# ============================================================
# 18. 자치구 고스트레스 유형 여가 비교
# ============================================================
st.header("8. 고스트레스 집단의 행복 수준별 여가 차이")

st.write(
    """
    고스트레스 집단 중에서도 행복 수준이 높은 집단과
    낮은 집단의 여가활동 차이를 비교합니다.
    """
)

hobby_type = stress_happiness_type.merge(
    hobby[
        ["구분", "구분상세"] + hobby_cols
    ],
    on=["구분", "구분상세"],
    how="inner",
)


selected_high_stress_hobby = hobby_type[
    (hobby_type["구분"] == selected_group)
    & (hobby_type["스트레스수준"] == "높음")
].copy()


if not selected_high_stress_hobby.empty:

    happiness_levels = set(
        selected_high_stress_hobby[
            "행복수준"
        ].dropna()
    )

    if {"높음", "낮음"}.issubset(
        happiness_levels
    ):

        hobby_compare = (
            selected_high_stress_hobby
            .groupby("행복수준")[
                hobby_cols
            ]
            .mean()
            .round(2)
        )

        st.subheader(
            "행복 수준별 여가활동 평균"
        )

        st.dataframe(
            hobby_compare,
            use_container_width=True,
        )

        hobby_diff = (
            hobby_compare.loc["높음"]
            - hobby_compare.loc["낮음"]
        ).round(2)

        hobby_diff = hobby_diff.sort_values(
            ascending=False
        )

        st.subheader(
            "고행복 - 저행복 차이"
        )

        st.bar_chart(hobby_diff)

    else:

        st.info(
            f"{selected_group}에서는 "
            "고스트레스 집단 중 고행복·저행복 유형이 "
            "모두 존재하지 않아 직접 비교하기 어렵습니다."
        )


# ============================================================
# 19. 분석 안내
# ============================================================
st.divider()

st.caption(
    """
    ※ 본 대시보드는 집단별 집계 통계를 비교한 것으로,
    고민·행복·여가활동과 스트레스 사이의
    인과관계를 의미하지 않습니다.
    """
)