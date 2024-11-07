import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import datetime

# Define the updated tasks and their start and finish dates based on the latest specifications
updated_tasks = {
    "Task": ["Enhance Visualization (v0.75)", "Algorithm Enhancement (v0.85)", "Performance Comparisons (v0.90)",
             "Requirements to Model Integration (v0.95)", "Enabling Studies (v1.0)", "Automation of Tasks (v1.1)",
             "Advanced Visualization (v1.5)", "Case Studies Part 1", "Case Studies Part 2", "Thesis and Paper Writing"],
    "Start": [datetime.date(2024, 10, 14), datetime.date(2024, 10, 29), datetime.date(2024, 11, 26),
              datetime.date(2024, 12, 10), datetime.date(2024, 12, 24), datetime.date(2025, 1, 7),
              datetime.date(2025, 2, 4), datetime.date(2025, 1, 6), datetime.date(2025, 1, 27), datetime.date(2025, 3, 15)],
    "Finish": [datetime.date(2024, 10, 28), datetime.date(2024, 11, 25), datetime.date(2024, 12, 9),
               datetime.date(2024, 12, 23), datetime.date(2025, 1, 6), datetime.date(2025, 2, 3),
               datetime.date(2025, 3, 2), datetime.date(2025, 1, 26), datetime.date(2025, 4, 27), datetime.date(2025, 6, 20)]
}

# Create a DataFrame from the updated tasks data
df_updated = pd.DataFrame(updated_tasks)

# Plotting
fig, ax = plt.subplots(figsize=(10, 8))
for i, task in df_updated.iterrows():
    start = mdates.date2num(task['Start'])
    finish = mdates.date2num(task['Finish'])
    ax.barh(task['Task'], finish - start, left=start, color='skyblue')

ax.set_title('PhD Project Gantt Chart holistic')
ax.set_xlabel('Date')
ax.set_ylabel('Tasks')
ax.set_xlim([mdates.date2num(datetime.date(2024, 10, 1)), mdates.date2num(datetime.date(2025, 8, 1))])
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Show plot
plt.show()
