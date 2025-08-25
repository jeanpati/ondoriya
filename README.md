##Build a pipeline in one day.

#Part 1: Data Ingestion
Your first task is to write a Python script to pull the dataset from its public R2 source and store it in a MinIO data lake. This simulates a real-world scenario where you need to move data from an external source into your own managed environment.
Objective
Write a Python script that:

- Defines the list of files to be downloaded.
- Loops through each file, downloading it from the public URL.
- Uploads each downloaded file to a specified MinIO bucket.

#Part 2: Data Storage and Modeling Plan
Now that the raw CSV files are in your MinIO data lake, you need to decide on a strategy for storing and querying them. The "best" choice depends what you want to personally use that you can accomplish this within the time frame

#Part 3: EDA & Visualization Plan
The final step is to analyze the data and present your findings. A dashboard is an effective way to summarize key metrics and trends.

Objective
Build a dashboard, here are some suggestions, use these or use your own.
Proposed Dashboard Metrics & Visualizations

1. Key Performance Indicators (KPIs)
   Total Population: A single number showing the sum of all individuals from the people.csv file.
   Dominant Faction: The name of the faction with the highest percentage from faction_distribution.csv.
2. Visualizations
   Population Density by Region
   Data: Use regions.csv and households.csv/people.csv to calculate population per region.
   Insight: Quickly show which regions of the planet are most heavily populated.
   Faction Distribution
   Data: Use faction_distribution.csv.
   Insight: Clearly compare the relative power and influence of each political faction.
   Top 5 Most Populous Regions
   Data: A sorted list derived from regions.csv and people.csv.
   Insight: Provide detailed, specific numbers for the most important regions.
