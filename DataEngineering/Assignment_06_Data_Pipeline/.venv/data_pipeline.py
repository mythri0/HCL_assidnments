
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

# ==================================================
# CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

EXCEL_FILE = BASE_DIR / "raw_sales_source_50_records_for_etl-1.xlsx"
DATABASE_PATH = BASE_DIR / "pipeline.db"

TABLE_NAME = "cleaned_data"


# ==================================================
# 1. INGESTION LAYER - READ RAW EXCEL FILE
# Library: Pandas
# ==================================================

def ingest_data():

    print("\n========== INGESTION LAYER ==========")

    if not EXCEL_FILE.exists():
        raise FileNotFoundError(
            f"Excel file not found: {EXCEL_FILE}"
        )

    df = pd.read_excel(EXCEL_FILE)

    if df.empty:
        raise ValueError("The input Excel file is empty.")

    print("Excel file loaded successfully.")
    print(f"Total records loaded: {len(df)}")
    print(f"Total columns: {len(df.columns)}")

    return df


# ==================================================
# 2. INTEGRATION LAYER - CLEAN AND TRANSFORM DATA
# Library: Pandas
# ==================================================

def clean_data(df):

    print("\n========== INTEGRATION LAYER ==========")

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )

    print("Column names standardized.")

    # Standardize date columns
    date_columns = [
        col for col in df.columns
        if "date" in col
    ]

    for col in date_columns:

        df[col] = pd.to_datetime(
            df[col],
            errors="coerce"
        ).dt.strftime("%Y-%m-%d")

    print(f"Date columns processed: {date_columns}")

    # Fill missing values
    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):

            df[col] = df[col].fillna(0)

        else:

            df[col] = df[col].fillna("Unknown")

    print("Missing values handled.")

    # Check remaining missing values
    missing_count = df.isnull().sum().sum()

    print(f"Remaining missing values: {missing_count}")
    print("Data cleaning completed successfully.")

    return df


# ==================================================
# 3. PRESENTATION LAYER - LOAD DATA INTO SQLITE
# Library: SQLAlchemy
# Database: SQLite
# ==================================================

def load_data(df):

    print("\n========== PRESENTATION LAYER ==========")

    engine = create_engine(
        f"sqlite:///{DATABASE_PATH}"
    )

    try:

        df.to_sql(
            TABLE_NAME,
            con=engine,
            if_exists="replace",
            index=False
        )

        print("Data inserted into SQLite successfully.")
        print(f"Database location: {DATABASE_PATH}")
        print(f"Table created: {TABLE_NAME}")

        return engine

    except Exception:

        engine.dispose()
        raise


# ==================================================
# 4. VALIDATION - VERIFY DATABASE RECORDS
# ==================================================

def validate_data(engine, expected_count):

    print("\n========== DATABASE VALIDATION ==========")

    with engine.connect() as connection:

        # Count database records
        count = connection.execute(
            text(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        ).scalar()

        # Display first five records
        result = pd.read_sql(
            f"SELECT * FROM {TABLE_NAME} LIMIT 5",
            connection
        )

        # Check table columns
        columns = connection.execute(
            text(f"PRAGMA table_info({TABLE_NAME})")
        ).fetchall()

    print(f"Expected records: {expected_count}")
    print(f"Inserted records: {count}")

    if count != expected_count:
        raise ValueError("Database record count mismatch!")

    print("\nDatabase table columns:")

    for column in columns:
        print(column[1])

    print("\nFirst 5 records from SQLite database:")
    print(result.to_string(index=False))

    print("\nDatabase validation successful!")


# ==================================================
# MAIN ETL PIPELINE
# ==================================================

def main():

    print("\n========================================")
    print("       PYTHON DATA ENGINEERING PIPELINE")
    print("========================================")

    engine = None

    try:

        # Step 1: Ingestion
        raw_df = ingest_data()

        # Step 2: Integration
        cleaned_df = clean_data(raw_df)

        # Step 3: Presentation
        engine = load_data(cleaned_df)

        # Step 4: Validation
        validate_data(
            engine,
            expected_count=len(cleaned_df)
        )

        print("\n========================================")
        print(" ETL PIPELINE COMPLETED SUCCESSFULLY!")
        print("========================================")

    except Exception as error:

        print("\nPIPELINE FAILED!")
        print(f"Error: {error}")
        raise

    finally:

        if engine is not None:
            engine.dispose()


# ==================================================
# EXECUTE PIPELINE
# ==================================================

if __name__ == "__main__":

    main()
