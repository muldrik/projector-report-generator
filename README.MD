# Projector stats report generator
This is a complementary set of scripts to generate graphs and metric reports on JetBrains Projector.

### Quick start
* Clone the `stats` branch of [this Projector fork](https://github.com/muldrik/projector-server)
* Run the app any number of times for 60 seconds: it will affect stabilize the average stats
* In this project, run `metricsTableMarkdown.py` to generate markdown tables for various metrics in the project. 
Example can be found in `CreateUpdateTable.md`
* run `plots.py` to generate plots for the last run. They include memory and network usage, as well as scatter plots
of operations that took unusually long time to complete. The plots will open automatically in your browser
