# src/preprocess.py

from pathlib import Path

import pandas as pd


# ============================================================
# 1. 경로 설정
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

COMMUTE_PATH = RAW_DIR / "commute.csv"
STRESS_PATH = RAW_DIR / "stress.csv"
HAPPINESS_PATH = RAW_DIR / "happiness.csv"


# ============================================================
# 2. 공통 전처리
# ============================================================

def clean_dataframe(df):
    # 컬럼명 공백 제거
    df.columns = (
        df.columns
        .str.replace("\xa0", " ", regex=False)
        .str.strip()
    )

    # 문자열 앞뒤 공백 제거
    text_columns = df.select_dtypes(include="object").columns

    for col in text_columns:
        df[col] = (
            df[col]
            .str.replace("\xa0", " ", regex=False)
            .str.strip()
        )

    # 완전히 비어 있는 행/열 제거
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    return df.reset_index(drop=True)


# ============================================================
# 3. 데이터 상태 확인
# ============================================================

def check_data(df, name):
    print(f"\n[{name}]")

    # 결측치
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    print("\n결측치")
    if missing.empty:
        print("없음")
    else:
        print(missing)

    # 중복값
    duplicate_count = df.duplicated().sum()

    print("\n중복 행")
    print(duplicate_count)

    # 숫자형 컬럼 기초통계
    numeric_columns = df.select_dtypes(include="number").columns

    print("\n수치형 데이터 기초통계")
    if len(numeric_columns) == 0:
        print("수치형 컬럼 없음")
    else:
        print(df[numeric_columns].describe())


# ============================================================
# 4. 이상치 확인
# ============================================================

def check_outliers(df):
    numeric_columns = df.select_dtypes(include="number").columns

    for col in numeric_columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = df[
            (df[col] < lower) |
            (df[col] > upper)
        ]

        if not outliers.empty:
            print(f"\n{col} 이상치 후보: {len(outliers)}개")
            print(outliers[[col]])


# ============================================================
# 5. 통근 데이터
# ============================================================

def preprocess_commute():
    df = pd.read_csv(COMMUTE_PATH)

    df = clean_dataframe(df)

    check_data(df, "통근 데이터")
    check_outliers(df)

    return df


# ============================================================
# 6. 스트레스 데이터
# ============================================================

def preprocess_stress():
    df = pd.read_csv(STRESS_PATH)

    df = clean_dataframe(df)

    check_data(df, "스트레스 데이터")
    check_outliers(df)

    return df


# ============================================================
# 7. 행복지수 데이터
# ============================================================

def preprocess_happiness():
    df = pd.read_csv(HAPPINESS_PATH)

    df = clean_dataframe(df)

    check_data(df, "행복지수 데이터")
    check_outliers(df)

    return df


# ============================================================
# 8. 저장
# ============================================================

def save_data(df, filename):
    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        PROCESSED_DIR / filename,
        index=False,
        encoding="utf-8-sig"
    )


# ============================================================
# 9. 실행
# ============================================================

def main():
    commute = preprocess_commute()
    stress = preprocess_stress()
    happiness = preprocess_happiness()

    save_data(
        commute,
        "commute_processed.csv"
    )

    save_data(
        stress,
        "stress_processed.csv"
    )

    save_data(
        happiness,
        "happiness_processed.csv"
    )


if __name__ == "__main__":
    main()