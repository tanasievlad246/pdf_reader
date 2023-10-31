import pdfplumber
import pandas as pd

# Extract tables using pdfplumber
def extract_tables_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = [page.extract_tables() for page in pdf.pages]

    # Flatten the list of tables since each page can have multiple tables
    tables_flattened = [table for sublist in all_tables for table in sublist]
    return tables_flattened

# Consolidate and clean the tables
def consolidate_tables(tables_flattened):
    renamed_columns = [
        "Cont", "Denumirea contului",
        "Sume precedente Debitoare", "Sume precedente Creditoare",
        "Rulaje perioada Debitoare", "Rulaje perioada Creditoare",
        "Sume totale Debitoare", "Sume totale Creditoare",
        "Solduri finale Debitoare", "Solduri finale Creditoare"
    ]

    consolidated_df = pd.DataFrame(columns=renamed_columns)
    for table in tables_flattened:
        temp_df = pd.DataFrame(table[1:], columns=table[0])
        temp_df.columns = renamed_columns
        temp_df = temp_df.dropna(subset=["Cont"])  # Drop rows with NaN in the "Cont" column
        consolidated_df = pd.concat([consolidated_df, temp_df], ignore_index=True)

    return consolidated_df

if __name__ == "__main__":
    pdf_path = "./saga.pdf"
    tables = extract_tables_from_pdf(pdf_path)
    consolidated_df = consolidate_tables(tables)

    # Export to CSV
    consolidated_df.to_csv("extracted_data.csv", index=False)