import sqlite3
import pandas as pd
from openpyxl import Workbook

def export_rate_analysis_to_excel(db_path, excel_path):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Define the tables to extract
        tables = ["Manpower", "Machines", "Materials"]

        # Create a new Excel writer
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            for table in tables:
                try:
                    # Fetch data from each table
                    query = f"SELECT level_type, unit, rate_per_unit FROM {table}"
                    df = pd.read_sql_query(query, conn)

                    # Drop duplicate level_type values, keeping the first occurrence
                    df = df.drop_duplicates(subset=["level_type"])

                    # Write to Excel sheet (one sheet per table)
                    df.to_excel(writer, sheet_name=table, index=False)

                    print(f"✅ Extracted and written table: {table}")

                except Exception as e:
                    print(f"⚠️ Error processing table {table}: {e}")

        print(f"\n📘 Data successfully exported to: {excel_path}")

    except Exception as e:
        print(f"❌ Database connection or export failed: {e}")

    finally:
        conn.close()

# _____________________________ USAGE _____________________________
if __name__ == "__main__":
    db_file = "DUDBC_RateAnalysis.db"
    output_excel = "RateAnalysis_Export.xlsx"
    export_rate_analysis_to_excel(db_file, output_excel)