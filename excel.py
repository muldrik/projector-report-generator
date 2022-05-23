import copy
from texttable import Texttable
import latextable
from tabulate import tabulate

from mdutils.mdutils import MdUtils
import pandas as pd
from io import StringIO

if __name__ == "__main__":

    with open("createUpdateMetrics.csv", "r") as f:
        joinedMetrics = f.read()

    separated = joinedMetrics.split("!\n")
    separated.pop()


    # create a csvList which consists of pd.read_csv(StringIO(csv)) for each csv in separated
    csvList = []
    for csv in separated:
        csvList.append(pd.read_csv(StringIO(csv)))

    # create a dataframe that has is a deepcopy of the first csv in csvList
    averaged = csvList[0].copy(deep=True)
    fst = csvList[0]

    print(fst["Value"])

    for i in range(fst.shape[0]):
        average = 0
        averageOfSquares = 0
        for csv in csvList:
            average += csv.iloc[i]["Value"]
            averageOfSquares += csv.iloc[i]["Value"] ** 2
        average /= len(csvList)
        averageOfSquares /= len(csvList)
        averaged.at[i, "Value"] = round(average, 1)
        if len(csvList) > 2:
            averaged.at[i, "Standard deviation"] = round((averageOfSquares - average**2) ** 0.5, 1)


    print(averaged)



    header = averaged.columns.values.tolist()
    values = averaged.values
    for value in values:
        value[1] = value[1].replace(";", ", ")
        value[1] = value[1].replace("Time threshold", "minTime")
        value[1] = value[1].replace("Objects threshold", "minObj")
    latexList = copy.deepcopy(values).tolist()
    latexHeader = copy.deepcopy(header)
    values = values.flatten().tolist()
    header.extend(values)

    latexList.insert(0, latexHeader)
    print(latexList)

    columns = len(averaged.columns.values)
    rows = len(header) // columns

    table = Texttable()
    table.set_cols_align(["c"] * 5)
    table.set_deco(Texttable.HEADER | Texttable.VLINES)
    table.add_rows(latexList)
    print(latextable.draw_latex(table, caption="Metrics table example"))

    print('\nTabulate Latex:')
    print(tabulate(latexList, headers='Metrics table example', tablefmt='latex'))

    mdFile = MdUtils(file_name='AwtTable',title='Awt processing')
    list_of_strings = ["Items", "Descriptions", "Data"]
    for x in range(5):
        list_of_strings.extend(["Item " + str(x), "Description Item " + str(x), str(x)])
    mdFile.new_line()
    mdFile.new_table(columns=columns, rows=rows, text=header, text_align='center')

    mdFile.create_md_file()