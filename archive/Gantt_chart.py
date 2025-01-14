
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import datetime

# Define the start date for the project
start_date = datetime.date.today()

# Define tasks and their durations
tasks_data = {
    "Task": ["Enhance Visualization", "Algorithm Enhancement", "Performance Comparisons",
             "Requirements to Model Integration", "Enabling Studies", "Automation of Tasks",
             "Advanced Visualization", "Case Studies"],
    "Start": [start_date, start_date + datetime.timedelta(weeks=2), start_date + datetime.timedelta(weeks=6),
              start_date + datetime.timedelta(weeks=8), start_date + datetime.timedelta(weeks=10),
              start_date + datetime.timedelta(weeks=12), start_date + datetime.timedelta(weeks=16),
              start_date + datetime.timedelta(weeks=20)],
    "Finish": [start_date + datetime.timedelta(weeks=2), start_date + datetime.timedelta(weeks=6),
               start_date + datetime.timedelta(weeks=8), start_date + datetime.timedelta(weeks=10),
               start_date + datetime.timedelta(weeks=12), start_date + datetime.timedelta(weeks=16),
               start_date + datetime.timedelta(weeks=20), start_date + datetime.timedelta(weeks=28)],
    "Version": ["v0.75", "v0.85", "v0.90", "v0.95", "v1.0", "v1.1", "v1.5", "Case Studies"]
}

# Create DataFrame
df = pd.DataFrame(tasks_data)

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(df['Task'], df['Finish'] - df['Start'], left=df['Start'], color='skyblue')
ax.set_title('PhD Project Gantt Chart without Extensions')
ax.set_xlabel('Date')
ax.set_ylabel('Tasks')
ax.set_xlim([start_date, start_date + datetime.timedelta(weeks=32)])
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_minor_locator(mdates.WeekdayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
plt.xticks(rotation=45)
plt.grid(True)

# Show plot
plt.show()