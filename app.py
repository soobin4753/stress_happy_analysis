import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
import streamlit as st


# ============================================================
# 1. 페이지 설정
# ============================================================

st.set_page_config(
    page_title="서울시민 스트레스와 생활 특성",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# 2. 데이터 불러오기
# ============================================================

stress = pd.read_csv("data/processed/stress_processed.csv")
happiness = pd.read_csv("data/processed/happiness_processed.csv")
hobby = pd.read_csv("data/processed/hobby_processed.csv")
worry = pd.read_csv("data/processed/worry_processed.csv")


# ============================================================
# 3. 분석 기준
# ============================================================

analysis_groups = ["성별", "연령별", "학력별", "소득별", "혼인상태별", "직업분류", "지역소분류"]

worry_cols = ["경제문제", "건강", "자녀양육", "노후생활", "가족문제", "공부", "진로", "결혼", "자기개발", "이성우정", "신체외모", "인터넷커뮤니티", "학교폭력", "기타"]

happiness_cols = ["건강상태", "재정상태", "친지친구관계", "가정생활", "사회생활"]

hobby_cols = ["관광", "스포츠활동", "문화예술관람", "문화예술참여", "스포츠관람", "취미오락", "휴식", "사회기타활동"]


# ============================================================
# 4. 전체 데이터 찾기
# ============================================================

def get_total_row(df):
    total_values = ["소계", "전체", "합계"]

    result = df[
        df["구분"].isin(total_values)
        | df["구분상세"].isin(total_values)
    ]

    return result.head(1)


total_stress = get_total_row(stress)
total_happiness = get_total_row(happiness)
total_hobby = get_total_row(hobby)
total_worry = get_total_row(worry)


# ============================================================
# 5. 소득별 고민 구간 일부 통합
# ============================================================

income_groups = {
    "200만원 미만": [
        "100만원 미만",
        "100-200만 미만"
    ],
    "200-400만원 미만": [
        "200-300만 미만",
        "300-400만 미만"
    ]
}

income_worry_rows = []

for new_group, old_groups in income_groups.items():

    income_data = worry[
        (worry["구분"] == "소득별")
        & (worry["구분상세"].isin(old_groups))
    ]

    if income_data.empty:
        continue

    row = income_data[worry_cols].mean()

    row["구분"] = "소득별"
    row["구분상세"] = new_group

    income_worry_rows.append(row)


if income_worry_rows:
    income_worry = pd.DataFrame(income_worry_rows)

    worry_dashboard = worry[
        worry["구분"] != "소득별"
    ].copy()

    worry_dashboard = pd.concat(
        [worry_dashboard, income_worry],
        ignore_index=True
    )

else:
    worry_dashboard = worry.copy()


# ============================================================
# 6. 스트레스 + 행복 데이터 결합
# ============================================================

stress_happiness = stress[
    ["구분", "구분상세", "스트레스체감률"]
].merge(
    happiness[
        ["구분", "구분상세", "행복지수"]
    ],
    on=["구분", "구분상세"],
    how="inner"
)


# ============================================================
# 7. 스트레스 + 행복 유형 생성
# ============================================================

type_results = []

for group_name in analysis_groups:

    group_data = stress_happiness[
        stress_happiness["구분"] == group_name
    ].copy()

    if group_data.empty:
        continue

    stress_mean = group_data["스트레스체감률"].mean()
    happiness_mean = group_data["행복지수"].mean()

    group_data["스트레스수준"] = group_data[
        "스트레스체감률"
    ].apply(
        lambda x: "높음" if x >= stress_mean else "낮음"
    )

    group_data["행복수준"] = group_data[
        "행복지수"
    ].apply(
        lambda x: "높음" if x >= happiness_mean else "낮음"
    )

    group_data["스트레스행복유형"] = (
        "스트레스 "
        + group_data["스트레스수준"]
        + " + 행복 "
        + group_data["행복수준"]
    )

    type_results.append(group_data)


stress_happiness_type = pd.concat(
    type_results,
    ignore_index=True
)


# ============================================================
# 8. 제목
# ============================================================

st.markdown(
    "<h1 style='text-align: center;'>서울시민 스트레스와 생활 특성</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>"
    "스트레스 수준과 고민·행복·여가 특성을 한눈에 확인합니다."
    "</p>",
    unsafe_allow_html=True
)


# ============================================================
# 9. 필터
# ============================================================

filter1, filter2 = st.columns(2)

with filter1:
    selected_group = st.selectbox(
        "분류 선택",
        analysis_groups
    )


group_stress = stress[
    stress["구분"] == selected_group
].copy()


detail_list = [
    value
    for value in group_stress["구분상세"].dropna().tolist()
    if value not in ["소계", "전체", "합계"]
]

detail_list = ["전체"] + detail_list


with filter2:
    selected_detail = st.selectbox(
        "세부 집단 선택",
        detail_list
    )


# ============================================================
# 10. 선택 집단 데이터
# ============================================================

if selected_detail == "전체":

    selected_stress = total_stress.copy()
    selected_happiness = total_happiness.copy()
    selected_worry = total_worry.copy()
    selected_hobby = total_hobby.copy()
    selected_type = pd.DataFrame()

else:

    selected_stress = stress[
        (stress["구분"] == selected_group)
        & (stress["구분상세"] == selected_detail)
    ]

    selected_happiness = happiness[
        (happiness["구분"] == selected_group)
        & (happiness["구분상세"] == selected_detail)
    ]

    selected_worry = worry_dashboard[
        (worry_dashboard["구분"] == selected_group)
        & (worry_dashboard["구분상세"] == selected_detail)
    ]

    selected_hobby = hobby[
        (hobby["구분"] == selected_group)
        & (hobby["구분상세"] == selected_detail)
    ]

    selected_type = stress_happiness_type[
        (stress_happiness_type["구분"] == selected_group)
        & (stress_happiness_type["구분상세"] == selected_detail)
    ]


# ============================================================
# 11. KPI
# ============================================================

stress_rate = (
    selected_stress.iloc[0]["스트레스체감률"]
    if not selected_stress.empty
    else None
)

happiness_score = (
    selected_happiness.iloc[0]["행복지수"]
    if not selected_happiness.empty
    else None
)


if not selected_worry.empty:

    worry_series = (
        selected_worry[worry_cols]
        .iloc[0]
        .dropna()
    )

    main_worry = (
        worry_series.idxmax()
        if not worry_series.empty
        else "-"
    )

else:
    main_worry = "비교 불가"


if selected_detail == "전체":
    stress_type = "전체"

elif not selected_type.empty:
    stress_type = selected_type.iloc[0]["스트레스행복유형"]

else:
    stress_type = "-"


kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    "스트레스체감률",
    f"{stress_rate:.1f}%"
    if stress_rate is not None
    else "-"
)

kpi2.metric(
    "행복지수",
    f"{happiness_score:.2f}"
    if happiness_score is not None
    else "-"
)

kpi3.metric(
    "주요 고민",
    main_worry
)

kpi4.metric(
    "스트레스·행복 유형",
    stress_type
)


st.divider()


# ============================================================
# 12. 그래프 1 + 2
# ============================================================

chart1, chart2 = st.columns(2)


# ------------------------------------------------------------
# 같은 분류의 스트레스 비교
# ------------------------------------------------------------

with chart1:

    st.subheader("같은 분류의 스트레스 비교")

    stress_chart = (
        group_stress[
            ["구분상세", "스트레스체감률"]
        ]
        .dropna()
        .sort_values(
            "스트레스체감률",
            ascending=False
        )
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=stress_chart,
        x="스트레스체감률",
        y="구분상세",
        ax=ax
    )

    ax.set_xlabel("스트레스체감률 (%)")
    ax.set_ylabel("")

    for container in ax.containers:
        ax.bar_label(
            container,
            fmt="%.1f%%",
            padding=3
        )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ------------------------------------------------------------
# 주요 고민 TOP 5
# ------------------------------------------------------------

with chart2:

    st.subheader("주요 고민 TOP 5")

    if not selected_worry.empty:

        top5_worry = (
            selected_worry[worry_cols]
            .iloc[0]
            .dropna()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )

        top5_worry.columns = [
            "고민",
            "비율"
        ]

        fig, ax = plt.subplots(figsize=(8, 5))

        sns.barplot(
            data=top5_worry,
            x="비율",
            y="고민",
            ax=ax
        )

        ax.set_xlabel("비율 (%)")
        ax.set_ylabel("")

        for container in ax.containers:
            ax.bar_label(
                container,
                fmt="%.1f%%",
                padding=3
            )

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)

    else:

        if selected_group == "소득별":
            st.info(
                "해당 소득구간은 고민 데이터와 "
                "동일한 구간으로 비교하기 어렵습니다."
            )

        else:
            st.info(
                "해당 집단의 고민 데이터가 없습니다."
            )


# ============================================================
# 13. 그래프 3 + 4
# ============================================================

chart3, chart4 = st.columns(2)


# ------------------------------------------------------------
# 행복 세부 영역
# ------------------------------------------------------------

with chart3:

    st.subheader("행복 세부 영역")

    if not selected_happiness.empty:

        happiness_detail = (
            selected_happiness[happiness_cols]
            .iloc[0]
            .dropna()
            .sort_values(ascending=False)
            .reset_index()
        )

        happiness_detail.columns = [
            "영역",
            "점수"
        ]

        fig, ax = plt.subplots(figsize=(8, 5))

        sns.barplot(
            data=happiness_detail,
            x="점수",
            y="영역",
            ax=ax
        )

        ax.set_xlabel("행복 점수")
        ax.set_ylabel("")

        for container in ax.containers:
            ax.bar_label(
                container,
                fmt="%.2f",
                padding=3
            )

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)

    else:
        st.info(
            "해당 집단의 행복 데이터가 없습니다."
        )


# ------------------------------------------------------------
# 여가생활
# ------------------------------------------------------------

with chart4:

    st.subheader("여가생활")

    if not selected_hobby.empty:

        hobby_detail = (
            selected_hobby[hobby_cols]
            .iloc[0]
            .dropna()
            .sort_values(ascending=False)
            .reset_index()
        )

        hobby_detail.columns = [
            "여가활동",
            "비율"
        ]

        fig, ax = plt.subplots(figsize=(8, 5))

        sns.barplot(
            data=hobby_detail,
            x="비율",
            y="여가활동",
            ax=ax
        )

        ax.set_xlabel("비율 (%)")
        ax.set_ylabel("")

        for container in ax.containers:
            ax.bar_label(
                container,
                fmt="%.1f%%",
                padding=3
            )

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)

    else:
        st.info(
            "해당 집단의 여가 데이터가 없습니다."
        )


# ============================================================
# 14. 선택 집단 한눈에 보기
# ============================================================

st.divider()

st.subheader("💡 선택 집단 한눈에 보기")


if selected_detail == "전체":

    if not selected_happiness.empty:
        lowest_happiness = (
            selected_happiness[happiness_cols]
            .iloc[0]
            .dropna()
            .idxmin()
        )
    else:
        lowest_happiness = "-"

    if not selected_hobby.empty:
        main_hobby = (
            selected_hobby[hobby_cols]
            .iloc[0]
            .dropna()
            .idxmax()
        )
    else:
        main_hobby = "-"

    st.info(
        f"서울시 전체 스트레스체감률은 "
        f"{stress_rate:.1f}%이며, "
        f"행복지수는 {happiness_score:.2f}입니다. "
        f"주요 고민은 {main_worry}이고, "
        f"행복 영역에서는 {lowest_happiness} 점수가 가장 낮으며, "
        f"여가활동에서는 {main_hobby} 비율이 가장 높게 나타났습니다."
    )


else:

    group_mean_stress = group_stress[
        "스트레스체감률"
    ].mean()

    stress_text = (
        "높은 편"
        if stress_rate >= group_mean_stress
        else "낮은 편"
    )

    happiness_level = (
        selected_type.iloc[0]["행복수준"]
        if not selected_type.empty
        else "-"
    )

    if not selected_happiness.empty:
        lowest_happiness = (
            selected_happiness[happiness_cols]
            .iloc[0]
            .dropna()
            .idxmin()
        )
    else:
        lowest_happiness = "-"

    if not selected_hobby.empty:
        main_hobby = (
            selected_hobby[hobby_cols]
            .iloc[0]
            .dropna()
            .idxmax()
        )
    else:
        main_hobby = "-"

    if main_worry == "비교 불가":

        st.info(
            f"{selected_detail}은 같은 {selected_group} 집단과 비교했을 때 "
            f"스트레스가 {stress_text}이며, "
            f"행복 수준은 {happiness_level}입니다. "
            f"행복 영역에서는 {lowest_happiness} 점수가 가장 낮고, "
            f"여가활동에서는 {main_hobby} 비율이 가장 높게 나타났습니다."
        )

    else:

        st.info(
            f"{selected_detail}(은/는) 같은 {selected_group} 집단과 비교했을 때 "
            f"스트레스가 {stress_text}이며, "
            f"행복 수준은 {happiness_level}입니다. "
            f"주요 고민은 {main_worry}이고, "
            f"행복 영역에서는 {lowest_happiness} 점수가 가장 낮으며, "
            f"여가활동에서는 {main_hobby} 비율이 가장 높게 나타났습니다."
        )


# ============================================================
# 15. 주의사항
# ============================================================

st.caption(
    "※ 본 대시보드는 집단별 통계를 비교한 것으로, "
    "고민·행복·여가활동과 스트레스 사이의 인과관계를 의미하지 않습니다. "
    "소득별 고민 데이터는 소득구간이 달라 비교 가능한 일부 구간만 "
    "단순 평균하여 참고용으로 구성했습니다."
)