import plotly.express as px
import pandas as pd
mem = pd.read_csv('memory.csv')
fig = px.line(mem, x="timestamp", y="value", color="type", labels={"value": "Memory Usage (MB)", "timestamp": "Time (ms)"})
fig.show()
