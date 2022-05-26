import pandas as pd
from io import StringIO

statsPath = "../projector-server/projector-server/outputStats/"


def separate_measurements(filename):
    with open(statsPath+filename, "r") as f:
        joinedMetrics = f.read()

    separated = joinedMetrics.split("!\n")
    separated.pop() # remove the last separator symbol
    return separated


def parse_time_metrics_file(filename):
    separated = separate_measurements(filename)

    # create a csvList which consists of measurements from all runs from the file in csv format
    csvList = []
    for csv in separated:
        csvList.append(pd.read_csv(StringIO(csv)))

    # create a dataframe that has is a deepcopy of the first csv in csvList
    averaged = csvList[0].copy(deep=True)
    fst = csvList[0]

    # calculate the average and standard deviation across all runs
    for i in range(fst.shape[0]):
        average = 0
        averageOfSquares = 0
        for csv in csvList:
            average += csv.iloc[i]["Value"]
            averageOfSquares += csv.iloc[i]["Value"] ** 2
        average /= len(csvList)
        averageOfSquares /= len(csvList)
        averaged.at[i, "Value"] = round(average, 1)
        averaged.at[i, "Standard deviation"] = round((averageOfSquares - average**2) ** 0.5, 1)

    averaged = averaged.reindex(columns=['Name', 'Params', 'Value', 'Measurement Unit', 'Standard deviation'])

    return averaged
