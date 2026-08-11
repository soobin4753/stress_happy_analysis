import pandas as pd

# ============================================================
# 1. 데이터 불러오기
# ============================================================

stress = pd.read_csv("data/raw/stress.csv")
happiness = pd.read_csv("data/raw/happiness.csv")
hobby = pd.read_csv("data/raw/hobby.csv")
worry = pd.read_csv("data/raw/worry.csv",)


# ============================================================
# 2. 컬럼명 정리
# ============================================================

stress = stress.rename(
    columns={
        "구분별(1)": "구분",
        "구분별(2)": "구분상세",
        "전혀 느끼지 않았다 (%)": "전혀안느낌",
        "느끼지 않은 편이다 (%)": "별로안느낌",
        "보통이다 (%)": "보통",
        "느낀 편이다 (%)": "느낀편",
        "매우 많이 느꼈다 (%)": "매우많이느낌",
        "10점 평균 (점)": "스트레스점수",
    }
)

happiness = happiness.rename(
    columns={
        "구분별(1)": "구분",
        "구분별(2)": "구분상세",
        "소계": "행복지수",
        "자신의 건강상태": "건강상태",
        "자신의 재정상태": "재정상태",
        "주위 친지 친구와의 관계": "친지친구관계",
        "가정생활": "가정생활",
        "사회생활": "사회생활",
    }
)

hobby = hobby.rename(
    columns={
        "구분별(1)": "구분",
        "구분별(2)": "구분상세",
        "관광(국내외 여행 캠핑 야외 나들이 등)": "관광",
        "스포츠 참여활동(축구 테니스 골프 수영 조깅 헬스 요가 등)": "스포츠활동",
        "문화예술 관람(영화 연극 전시회 연주회 콘서트 등)": "문화예술관람",
        "문화예술 참여활동(문학행사 미술 악기연주 무용/댄스 사진 등)": "문화예술참여",
        "스포츠 관람(경기장 직접관람 미디어 통한 간접관람 e-스포츠 경기 포함)": "스포츠관람",
        "취미/오락활동(생활공예 독서 온라인게임 인터넷검색 쇼핑/외식 등)": "취미오락",
        "휴식 활동(산책 낮잠 TV시청 모바일컨텐츠/OTT시청 음악감상 아무것도 안하기 등)": "휴식",
        "사회 및 기타 활동(자원봉사 모임 종교활동 기타 여가활동 등)": "사회기타활동",
    }
)

worry = worry.rename(
    columns={
        "구분별(1)": "구분",
        "구분별(2)": "구분상세",
        "계": "전체",
        "경제 관련 문제": "경제문제",
        "건강": "건강",
        "자녀양육": "자녀양육",
        "노후생활": "노후생활",
        "가족간 문제": "가족문제",
        "공부": "공부",
        "진학 취업 은퇴 등 진로선택": "진로",
        "본인 및 가족의 결혼": "결혼",
        "자기개발": "자기개발",
        "고민없음": "고민없음",
        "이성 및 우정 문제": "이성우정",
        "신체 외모": "신체외모",
        "인터넷 커뮤니티": "인터넷커뮤니티",
        "학교(원) 폭력": "학교폭력",
        "기타": "기타",
    }
)


# ============================================================
# 3. 문자열 공백 제거
# ============================================================

def clean_strip(df):
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()


clean_strip(stress)
clean_strip(happiness)
clean_strip(hobby)
clean_strip(worry)


# ============================================================
# 4. 분류명 일부 통일
# ============================================================

# 고민 데이터와 2025 데이터 사이에
# 이름만 다른 항목은 같은 이름으로 맞춤

worry["구분상세"] = worry["구분상세"].replace(
    {
        "남자": "남성",
        "여자": "여성",
        "60대 이상": "60세 이상",
        "중졸 이하": "중학교 이하",
    }
)


# ============================================================
# 5. 중복값 확인
# ============================================================

def check_duplicates(df, name):
    duplicated = df[df.duplicated()]

    print(f"\n===== {name} 중복값 =====")
    print("중복값 개수:", len(duplicated))

    if len(duplicated) > 0:
        print(duplicated)


check_duplicates(stress, "stress")
check_duplicates(happiness, "happiness")
check_duplicates(hobby, "hobby")
check_duplicates(worry, "worry")


# ============================================================
# 6. 특수값 처리
# ============================================================

# 고민 데이터의 '-'는 값이 없음을 의미하므로 결측치 처리
worry = worry.replace("-", pd.NA)


# ============================================================
# 7. 숫자형 변환
# ============================================================

stress_numeric_cols = [
    "전혀안느낌",
    "별로안느낌",
    "보통",
    "느낀편",
    "매우많이느낌",
    "스트레스점수",
]

happiness_numeric_cols = [
    "행복지수",
    "건강상태",
    "재정상태",
    "친지친구관계",
    "가정생활",
    "사회생활",
]

hobby_numeric_cols = [
    "관광",
    "스포츠활동",
    "문화예술관람",
    "문화예술참여",
    "스포츠관람",
    "취미오락",
    "휴식",
    "사회기타활동",
]

concern_numeric_cols = [
    "전체",
    "경제문제",
    "건강",
    "자녀양육",
    "노후생활",
    "가족문제",
    "공부",
    "진로",
    "결혼",
    "자기개발",
    "고민없음",
    "이성우정",
    "신체외모",
    "인터넷커뮤니티",
    "학교폭력",
    "기타",
]


stress[stress_numeric_cols] = (
    stress[stress_numeric_cols]
    .apply(pd.to_numeric, errors="coerce")
)

happiness[happiness_numeric_cols] = (
    happiness[happiness_numeric_cols]
    .apply(pd.to_numeric, errors="coerce")
)

hobby[hobby_numeric_cols] = (
    hobby[hobby_numeric_cols]
    .apply(pd.to_numeric, errors="coerce")
)

worry[concern_numeric_cols] = (
    worry[concern_numeric_cols]
    .apply(pd.to_numeric, errors="coerce")
)


# ============================================================
# 8. 숫자형 변환 후 결측치 확인
# ============================================================

def check_missing(df, name):
    print(f"\n===== {name} 결측치 =====")
    print(df.isnull().sum())


check_missing(stress, "stress")
check_missing(happiness, "happiness")
check_missing(hobby, "hobby")
check_missing(worry, "worry")


# ============================================================
# 9. 파생변수 생성
# ============================================================

# 스트레스를 느낀다고 응답한 비율

stress["스트레스체감률"] = (
    stress["느낀편"]
    + stress["매우많이느낌"]
).round(1)


# ============================================================
# 10. 구분 값 확인
# ============================================================

print("\n===== stress 구분 =====")
print(stress["구분"].value_counts())

print("\n===== happiness 구분 =====")
print(happiness["구분"].value_counts())

print("\n===== hobby 구분 =====")
print(hobby["구분"].value_counts())

print("\n===== concern 구분 =====")
print(worry["구분"].value_counts())


# ============================================================
# 11. 네 데이터 공통 구분 확인
# ============================================================

common_groups = (
    set(stress["구분"].dropna().unique())
    & set(happiness["구분"].dropna().unique())
    & set(hobby["구분"].dropna().unique())
    & set(worry["구분"].dropna().unique())
)

print("\n===== 공통 구분 =====")
print(sorted(common_groups))


# ============================================================
# 12. 전처리 데이터 저장
# ============================================================

stress.to_csv(
    "data/processed/stress_processed.csv",
    index=False,
    encoding="utf-8-sig"
)

happiness.to_csv(
    "data/processed/happiness_processed.csv",
    index=False,
    encoding="utf-8-sig"
)

hobby.to_csv(
    "data/processed/hobby_processed.csv",
    index=False,
    encoding="utf-8-sig"
)

worry.to_csv(
    "data/processed/worry_processed.csv",
    index=False,
    encoding="utf-8-sig"
)