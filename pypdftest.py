import tabula
from pandas import DataFrame

# Read pdf into a list of DataFrame
dfs = tabula.read_pdf("./saga.pdf", pages='all', multiple_tables=True, guess=True)

def combine_rows(row1, row2):
    row1 = frame.iloc[0].values.flatten().tolist()
    row2 = frame.iloc[1].values.flatten().tolist()
    new_row = row1 + row2
    new_row = [x for x in new_row if str(x) != 'nan']
    return new_row

def rename_df(frame: DataFrame, new_header):
    rename_dict = { col: col for col in frame.columns }
    print(rename_dict)
    for [key, value], _value in zip(rename_dict.items(), new_header):
        rename_dict[key] = _value
    print("rename_dict", rename_dict)
    frame.rename(columns=rename_dict, inplace=True)

for index in range(len(dfs)):
    frame = DataFrame(dfs[index])
    print("===============", index, "===============")
    if index == 0:
        new_header = combine_rows(frame.iloc[0], frame.iloc[1])
        print("new_header", new_header)
        # frame.drop([0, 1], axis=0, inplace=True)
        # frame.columns = new_header
        # frame['Debitoare Creditoare'] = frame['Debitoare Creditoare'].astype(str)
        # frame[['Debitoare', 'Creditoare']] = frame['Debitoare Creditoare'].str.split(' ', expand=True)
    # If next dataframes column names start with "Cont", "Denumirea clientului"
    print(frame)

# convert PDF into CSV
tabula.convert_into("./saga.pdf", "output.csv", output_format="csv", pages='all')

# convert all PDFs in a directory
# tabula.convert_into_by_batch("input_directory", output_format='csv', pages='all')

