import plotly.express as px
import pandas as pd

kek = pd.read_csv("network.csv")

# Create an empty dataframe with columns timestamp and value

df = pd.DataFrame(columns=['timestamp', 'bytes'])

for i in range(0, 60):
    # sum all values in kek with timestamps from i*1000 to (i+1)*1000
    # save into an int
    print("---", len(df))
    summed = kek[(kek['timestamp'] >= i*1000) & (kek['timestamp'] < (i+1)*1000)].sum()['bytes']
    summed = summed // 1024 # In kilobytes
    print(summed)
    # add a row to df with timestamp i and 'bytes' summed
    df.loc[len(df)] = [i, summed]

print(df)

print(len(kek['timestamp']))

if __name__ == "__main__":
    fig = px.line(df, x='timestamp', y='bytes', labels={'bytes': 'Kb/s'})
    #fig = px.scatter(kek, x='timestamp', y='bytes')
    fig.show()


