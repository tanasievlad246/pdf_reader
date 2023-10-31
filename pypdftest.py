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
    print(frame)


# convert PDF into CSV
tabula.convert_into("./saga.pdf", "output.csv", output_format="csv", pages='all')


