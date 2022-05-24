import plotly.express as px
import pandas as pd

import common


def scatter_time(filename, title):
    data = pd.read_csv(common.statsPath+filename)
    fig = px.scatter(data, title=title, x="timestamp", y="len", color="task", size="len", size_max=25, labels={"len": "Operation time (ms)"})
    fig.show()


def network(filename, measurement_len_seconds):
    data = pd.read_csv("network.csv")

    # A new dataframe to store the average network usage
    result = pd.DataFrame(columns=['timestamp', 'bytes'])

    for i in range(0, measurement_len_seconds):
        # sum all values in data with timestamps from i*1000 to (i+1)*1000
        summed = data[(data['timestamp'] >= i * 1000) & (data['timestamp'] < (i + 1) * 1000)].sum()['bytes']
        summed = summed // 1024  # In kilobytes
        # add a row to result with timestamp i and 'bytes' summed
        result.loc[len(result)] = [i, summed]

    fig_average = px.line(result, x='timestamp', y='bytes', labels={'bytes': 'Kb/s'})
    fig_packets = px.scatter(data, x='timestamp', y='bytes')
    fig_average.show()
    fig_packets.show()


def memory(filename):
    mem = pd.read_csv(common.statsPath+filename)
    fig = px.line(mem, x="timestamp", y="value", color="type",
                  labels={"value": "Memory Usage (MB)", "timestamp": "Time (ms)"})
    fig.show()


if __name__ == "__main__":
    scatter_time("createUpdateForPlotting.csv", "createUpdate peaks")
    scatter_time("awtForPlotting.csv", "Awt peaks")
    network("networkForPlotting.csv", 60)
    memory("memoryForPlotting.csv")
