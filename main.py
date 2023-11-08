import pdfplumber
import pandas as pd
import sys
import pprint

def get_columns(model="saga"):
    if model == "saga":
        return [
        "Cont", "Denumirea contului",
        "Sume precedente Debitoare", "Sume precedente Creditoare",
        "Rulaje perioada Debitoare", "Rulaje perioada Creditoare",
        "Sume totale Debitoare", "Sume totale Creditoare",
        "Solduri finale Debitoare", "Solduri finale Creditoare"
    ]
    elif model == "keez":
        return [
        "Cont", "Denumirea contului",
        "Solduri Initiale Debitoare", "Solduri Initiale Creditoare",
        "Rulaje anterioare Debitoare", "Rulaje anterioare Creditoare",
        "Rulaje curente Debitoare", "Rulaje curente Creditoare",
        "Total sume Debitoare", "Total sume Creditoare",
        "Solduri finale Debitoare", "Solduri finale Creditoare",
    ]
    elif model == "winmentor":
        return [
        "Cont", "Denumirea contului",
        "Solduri Initiale Debitoare", "Solduri Initiale Creditoare",
        "Rulaje precedente Debitoare", "Rulaje precedente Creditoare",
        "Rulaje curente Debitoare", "Rulaje curente Creditoare",
        "Rulaj cumulat Debitoare", "Rulaj cumulat Creditoare",
        "Total sume Debitoare", "Total sume Creditoare",
        "Solduri finale Debitoare", "Solduri finale Creditoare",
    ]

# Extract tables using pdfplumber
def extract_tables_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = [page.extract_tables() for page in pdf.pages]

    # Flatten the list of tables since each page can have multiple tables
    tables_flattened = [table for sublist in all_tables for table in sublist]
    return tables_flattened

def process_list(input_list, columns_count):
    # Check if the list has more than 12 elements

    if len(input_list) > columns_count:
        # Remove the None value if present
        input_list = [item for item in input_list if item is not None]
    # Check if the list has less than 12 elements
    elif len(input_list) < columns_count:
        # Add 'Lipsa' at the end of the list
        input_list.append('Lipsa')
    return input_list

def process_keez(tables_flattened, renamed_columns):
    consolidated_df = pd.DataFrame(columns=renamed_columns)
    for table in tables_flattened:
        # drop all None values from the sublists of table
        new_table = []
        for sublist in table:
            new_sublist = process_list(sublist, 12)
            if len(new_sublist) == 12:
                new_table.append(new_sublist)
            elif len(new_sublist) != 12:
                print('Rand cu erroare non conforma \n', new_sublist)
        temp_df = pd.DataFrame(new_table[1:], columns=new_table[0])
        temp_df.columns = renamed_columns
        temp_df = temp_df.dropna(subset=["Cont"])  # Drop rows with NaN in the "Cont" column
        consolidated_df = pd.concat([consolidated_df, temp_df], ignore_index=True)

    return consolidated_df

def process_saga(tables_flattened, renamed_columns):
    consolidated_df = pd.DataFrame(columns=renamed_columns)
    for table in tables_flattened:
        temp_df = pd.DataFrame(table[1:], columns=table[0])
        temp_df.columns = renamed_columns
        temp_df = temp_df.dropna(subset=["Cont"])  # Drop rows with NaN in the "Cont" column
        consolidated_df = pd.concat([consolidated_df, temp_df], ignore_index=True)

    return consolidated_df

def process_winmentor(tables_flattened, renamed_columns):
    consolidated_df = pd.DataFrame(columns=renamed_columns)
    for table in tables_flattened:
    # drop all None values from the sublists of table
        new_table = []
        for sublist in table:
            new_sublist = process_list(sublist, 14)
            if len(new_sublist) == 14:
                new_table.append(new_sublist)
            elif len(new_sublist) != 14:
                print('Rand cu erroare non conforma \n', new_sublist)
    temp_df = pd.DataFrame(new_table[1:], columns=new_table[0])
    temp_df.columns = renamed_columns
    temp_df = temp_df.dropna(subset=["Cont"])  # Drop rows with NaN in the "Cont" column
    consolidated_df = pd.concat([consolidated_df, temp_df], ignore_index=True)

    return consolidated_df


# Consolidate and clean the tables
def consolidate_tables(tables_flattened, model="saga"):
    renamed_columns = get_columns(model)

    if model == "saga":
        return process_saga(tables_flattened, renamed_columns)
    elif model == "keez":
        return process_keez(tables_flattened, renamed_columns)
    elif model == "winmentor":
        return process_winmentor(tables_flattened, renamed_columns)

if __name__ == "__main__":
    # get the first argument and pass it to the pdf_path variable
    pdf_path = sys.argv[1]
    model = sys.argv[2]

    if pdf_path.lower() == "help":
        print("""
            Folosire: python main.py <calea catre fisierul PDF> <model> (saga, keez, winmentor)
              """)

    if not pdf_path:
        raise Exception("You must provide a PDF path")

    tables = extract_tables_from_pdf(pdf_path)
    consolidated_df = consolidate_tables(tables, model)

    print(consolidated_df)

    # Export to CSV
    consolidated_df.to_csv(f"{model}_extract.csv", index=False)