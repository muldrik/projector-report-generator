import plotly.express as px
import pandas as pd
df = px.data.iris() # iris is a pandas DataFrame


kek = pd.read_csv("createUpdateTime.csv")
print(kek.columns.values.tolist())
print(kek.values.tolist())
#fig = px.bar(kek, x="timestamp", y="len", color="task", width=[0.5]*len(kek))
#kek = kek.drop(kek[kek.len < 8].index)
# drop all rows with task == "Calculate main window shift"
#kek = kek.drop(kek[kek.task == "Calculate main window shift"].index)
#kek = kek.drop(kek[kek.task == "Collect Garbage"].index)

# subtract first timestamp from all timestamps
mn = kek["timestamp"].min()
kek["timestamp"] = kek["timestamp"] - mn
fig2 = px.bar(kek, x="timestamp", y="len", color="task", labels={"len": "Operation time (ms)"})
fig = px.scatter(kek, x="timestamp", y="len", color="task", size="len", size_max=25, labels={"len": "Operation time (ms)"})
fig.show()

