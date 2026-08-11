import pandas as pd
import numpy as np

# 데이터 불러오기
commute = pd.read_csv("data/raw/commute.csv")
stress = pd.read_csv("data/raw/stress.csv")
happiness = pd.read_csv("data/raw/happiness.csv")
hobby = pd.read_csv("data/raw/hobby.csv")

# 데이터 구조 확인
# print(commute.shape)
# print(commute.columns)
# print(stress.shape)
# print(stress.columns)
# print(happiness.shape)
# print(happiness.columns)
# print(hobby.shape)
# print(hobby.columns)

# 컬럼명 정리
# 분석할 때 사용하기 쉽도록 길거나 복잡한 컬럼명을 간단하게 변경

# 1. 통근·통학시간 데이터
commute = commute.rename(
    columns={
        "구분별(1)": "구분",
        "구분별(2)": "구분상세",
        "30분 미만 (%)": "30분미만",
        "30분-1시간 미만 (%)": "30분_1시간",
        "1시간-1시간 30분 미만 (%)": "1시간_1시간30분",
        "1시간 30분-2시간 미만 (%)": "1시간30분_2시간",
        "2시간 이상 (%)": "2시간이상",
        "평균소요시간 (분)": "평균통근시간",
    }
)

#print("commute")
#print(commute.columns.tolist())


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

# print("stress")
# print(stress.columns.tolist())

happiness = happiness.rename(
    columns={
        "구분별(1)": "구분",
        "구분별(2)": "구분상세",
        "소계" : "행복지수",
        "자신의 건강상태": "건강상태",
        "자신의 재정상태": "재정상태",
        "주위 친지 친구와의 관계": "친지친구관계",
        "가정생활": "가정생활",
        "사회생활": "사회생활",
    }
)

# print("happiness")
# print(happiness.columns.tolist())

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

# print("hobby")
# print(hobby.columns.tolist())


# 문자열 컬럼 값의 앞뒤 공백 제거
def clean_strip(df):
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()

clean_strip(commute)
clean_strip(stress)
clean_strip(happiness)
clean_strip(hobby)


# 결측치 확인
# 4개의 데이터 결측치 없음 확인
def check_missing(df, name):
    print(f"\n===== {name} 결측치 =====")
    print(df.isnull().sum())

check_missing(commute, "commute")
check_missing(stress, "stress")
check_missing(happiness, "happiness")
check_missing(hobby, "hobby")


# 중복값 확인
# 4개의 데이터 중복값 없음 확인
def check_duplicates(df, name):
    print(f"\n===== {name} 중복값 =====")
    
    duplicated = df[df.duplicated()]
    
    print("중복값 개수:", len(duplicated))
    print(duplicated)


check_duplicates(commute, "commute")
check_duplicates(stress, "stress")
check_duplicates(happiness, "happiness")
check_duplicates(hobby, "hobby")


# 특수값 확인
# commute 데이터의 '-' 값은 해당 구간의 비율이 없는 경우이므로 0으로 처리
commute = commute.replace("-", 0)


# 7. 숫자형 변환
commute_numeric_cols = [
    "30분미만",
    "30분_1시간",
    "1시간_1시간30분",
    "1시간30분_2시간",
    "2시간이상",
    "평균통근시간",
]

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


commute[commute_numeric_cols] = commute[
    commute_numeric_cols
].apply(pd.to_numeric, errors="coerce")

stress[stress_numeric_cols] = stress[
    stress_numeric_cols
].apply(pd.to_numeric, errors="coerce")

happiness[happiness_numeric_cols] = happiness[
    happiness_numeric_cols
].apply(pd.to_numeric, errors="coerce")

hobby[hobby_numeric_cols] = hobby[
    hobby_numeric_cols
].apply(pd.to_numeric, errors="coerce")



# 8. 파생변수 생성
# 1시간 이상 통근하는 비율
commute["장시간통근율"] = (
    commute["1시간_1시간30분"]
    + commute["1시간30분_2시간"]
    + commute["2시간이상"]
).round(1)

# 스트레스를 느낀다고 응답한 비율
stress["스트레스체감률"] = (
    stress["느낀편"]
    + stress["매우많이느낌"]
).round(1)


# 9. 전처리 결과 확인
print("\n===== commute =====")
print(
    commute[
        [
            "구분",
            "구분상세",
            "평균통근시간",
            "장시간통근율",
        ]
    ].head()
)

print("\n===== stress =====")
print(
    stress[
        [
            "구분",
            "구분상세",
            "스트레스점수",
            "스트레스체감률",
        ]
    ].head()
)

print("\n===== happiness =====")
print(
    happiness[
        [
            "구분",
            "구분상세",
            "행복지수",
        ]
    ].head()
)

print("\n===== hobby =====")
print(hobby.head())

commute.to_csv(
    "data/processed/commute_processed.csv",
    index=False,
    encoding="utf-8-sig"
)

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

