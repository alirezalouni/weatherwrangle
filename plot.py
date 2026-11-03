import json
import datetime
from collections import Counter
import math

# Load data
print("Loading data...")
records = [json.loads(line) for line in open("daily_14.json") if line.strip()]

# ============================================================
# Chart 1: San Francisco - temp.min and temp.max by date
# ============================================================
print("Creating Chart 1: San Francisco temperature range...")
sf_dates = []
sf_temps_min = []
sf_temps_max = []

for record in records:
    if record["city"]["id"] == 5391959:  # San Francisco
        for day in record["data"]:
            dt_obj = datetime.datetime.utcfromtimestamp(day["dt"])
            sf_dates.append(dt_obj)
            sf_temps_min.append(day["temp"]["min"] - 273.15)
            sf_temps_max.append(day["temp"]["max"] - 273.15)
        break

# Create SVG for Chart 1
width, height = 1000, 500
padding = 80
plot_width = width - 2*padding
plot_height = height - 2*padding

min_date = min(sf_dates)
max_date = max(sf_dates)
min_temp = min(sf_temps_min)
max_temp = max(sf_temps_max)

date_range = (max_date - min_date).days
temp_range = max_temp - min_temp + 2

svg1 = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .grid {{ stroke: #ddd; }}
    .axis {{ stroke: black; stroke-width: 2; }}
    .line-min {{ stroke: blue; stroke-width: 2; fill: none; }}
    .line-max {{ stroke: red; stroke-width: 2; fill: none; }}
    .grid-text {{ font-size: 11px; text-anchor: middle; }}
    .title {{ font-size: 18px; font-weight: bold; text-anchor: middle; }}
    .label {{ font-size: 14px; font-weight: bold; }}
  </style>

  <!-- Title -->
  <text x="{width/2}" y="30" class="title">San Francisco (CA, US): Min/Max Daily Temperature</text>

  <!-- Y-axis label -->
  <text x="20" y="{height/2}" text-anchor="middle" transform="rotate(-90 20 {height/2})" class="label">Temperature (°C)</text>

  <!-- X-axis label -->
  <text x="{width/2}" y="{height-10}" text-anchor="middle" class="label">Date</text>

  <!-- Grid and axes -->
  <line x1="{padding}" y1="{padding}" x2="{padding}" y2="{padding+plot_height}" class="axis"/>
  <line x1="{padding}" y1="{padding+plot_height}" x2="{padding+plot_width}" y2="{padding+plot_height}" class="axis"/>
'''

# Add grid lines and labels
for i in range(len(sf_dates)):
    x = padding + (i / (len(sf_dates) - 1)) * plot_width
    svg1 += f'  <line x1="{x}" y1="{padding}" x2="{x}" y2="{padding+plot_height}" class="grid" stroke-dasharray="2,2"/>\n'

for i in range(6):
    temp = min_temp + (i / 5) * temp_range
    y = padding + plot_height - (i / 5) * plot_height
    svg1 += f'  <line x1="{padding}" y1="{y}" x2="{padding+plot_width}" y2="{y}" class="grid" stroke-dasharray="2,2"/>\n'
    svg1 += f'  <text x="{padding-10}" y="{y+4}" text-anchor="end" class="grid-text">{temp:.1f}</text>\n'

# Add date labels
for i in range(0, len(sf_dates), max(1, len(sf_dates)//6)):
    x = padding + (i / (len(sf_dates) - 1)) * plot_width if len(sf_dates) > 1 else padding
    date_str = sf_dates[i].strftime("%m-%d")
    svg1 += f'  <text x="{x}" y="{padding+plot_height+20}" class="grid-text">{date_str}</text>\n'

# Plot lines
if len(sf_dates) > 1:
    points_min = ' '.join([f"{padding + (i/(len(sf_dates)-1))*plot_width},{padding+plot_height-(sf_temps_min[i]-min_temp)/temp_range*plot_height}"
                           for i in range(len(sf_dates))])
    points_max = ' '.join([f"{padding + (i/(len(sf_dates)-1))*plot_width},{padding+plot_height-(sf_temps_max[i]-min_temp)/temp_range*plot_height}"
                           for i in range(len(sf_dates))])

    svg1 += f'  <polyline points="{points_min}" class="line-min"/>\n'
    svg1 += f'  <polyline points="{points_max}" class="line-max"/>\n'

    # Add legend
    svg1 += f'''  <rect x="{width-150}" y="50" width="140" height="60" fill="white" stroke="black" stroke-width="1"/>
  <line x1="{width-140}" y1="65" x2="{width-110}" y2="65" class="line-min"/>
  <text x="{width-105}" y="70" font-size="12">Temp Min</text>
  <line x1="{width-140}" y1="85" x2="{width-110}" y2="85" class="line-max"/>
  <text x="{width-105}" y="90" font-size="12">Temp Max</text>
'''

svg1 += '</svg>'

with open('plot_1_sf_temperature.svg', 'w') as f:
    f.write(svg1)
print("✓ Chart 1 saved: plot_1_sf_temperature.svg")

# ============================================================
# Chart 2: Histogram of temp.day in Celsius across all city days
# ============================================================
print("Creating Chart 2: Histogram of daytime temperatures...")
all_temps_day = []

for record in records:
    for day in record["data"]:
        temp_day_c = day["temp"]["day"] - 273.15
        all_temps_day.append(temp_day_c)

# Create histogram
bins = 50
min_temp_all = min(all_temps_day)
max_temp_all = max(all_temps_day)
bin_width = (max_temp_all - min_temp_all) / bins
bin_counts = [0] * bins

for temp in all_temps_day:
    bin_idx = min(int((temp - min_temp_all) / bin_width), bins - 1)
    bin_counts[bin_idx] += 1

max_count = max(bin_counts)
mean_temp = sum(all_temps_day) / len(all_temps_day)

width2, height2 = 1000, 500
padding2 = 80
plot_width2 = width2 - 2*padding2
plot_height2 = height2 - 2*padding2
bar_width = plot_width2 / bins * 0.9

svg2 = f'''<svg width="{width2}" height="{height2}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .grid {{ stroke: #ddd; }}
    .axis {{ stroke: black; stroke-width: 2; }}
    .bar {{ fill: coral; stroke: black; stroke-width: 0.5; }}
    .mean-line {{ stroke: red; stroke-width: 2; stroke-dasharray: 4,4; }}
    .grid-text {{ font-size: 11px; text-anchor: middle; }}
    .title {{ font-size: 18px; font-weight: bold; text-anchor: middle; }}
    .label {{ font-size: 14px; font-weight: bold; }}
  </style>

  <!-- Title -->
  <text x="{width2/2}" y="30" class="title">Distribution of Daytime Temperature Across All Cities (n={len(all_temps_day):,} days)</text>

  <!-- Y-axis label -->
  <text x="20" y="{height2/2}" text-anchor="middle" transform="rotate(-90 20 {height2/2})" class="label">Frequency (number of days)</text>

  <!-- X-axis label -->
  <text x="{width2/2}" y="{height2-10}" text-anchor="middle" class="label">Temperature (°C)</text>

  <!-- Axes -->
  <line x1="{padding2}" y1="{padding2}" x2="{padding2}" y2="{padding2+plot_height2}" class="axis"/>
  <line x1="{padding2}" y1="{padding2+plot_height2}" x2="{padding2+plot_width2}" y2="{padding2+plot_height2}" class="axis"/>
'''

# Add grid lines
for i in range(6):
    y = padding2 + plot_height2 - (i / 5) * plot_height2
    svg2 += f'  <line x1="{padding2}" y1="{y}" x2="{padding2+plot_width2}" y2="{y}" class="grid" stroke-dasharray="2,2"/>\n'
    count_label = int(i / 5 * max_count)
    svg2 += f'  <text x="{padding2-10}" y="{y+4}" text-anchor="end" class="grid-text">{count_label:,}</text>\n'

# Add bars
for i, count in enumerate(bin_counts):
    x = padding2 + (i / bins) * plot_width2 + (plot_width2 / bins - bar_width) / 2
    bar_height = (count / max_count) * plot_height2 if max_count > 0 else 0
    y = padding2 + plot_height2 - bar_height
    svg2 += f'  <rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" class="bar"/>\n'

# Add temperature labels on x-axis
for i in range(0, bins, max(1, bins//8)):
    temp_label = min_temp_all + (i / bins) * (max_temp_all - min_temp_all)
    x = padding2 + (i / bins) * plot_width2
    svg2 += f'  <text x="{x}" y="{padding2+plot_height2+20}" class="grid-text">{temp_label:.0f}</text>\n'

# Add mean line
mean_x = padding2 + ((mean_temp - min_temp_all) / (max_temp_all - min_temp_all)) * plot_width2
svg2 += f'  <line x1="{mean_x}" y1="{padding2}" x2="{mean_x}" y2="{padding2+plot_height2}" class="mean-line"/>\n'
svg2 += f'  <text x="{mean_x+5}" y="{padding2+20}" font-size="12" fill="red">Mean: {mean_temp:.2f}°C</text>\n'

svg2 += '</svg>'

with open('plot_2_temp_day_histogram.svg', 'w') as f:
    f.write(svg2)
print("✓ Chart 2 saved: plot_2_temp_day_histogram.svg")

# ============================================================
# Chart 3: Bar chart of forecast length distribution
# ============================================================
print("Creating Chart 3: Forecast length distribution...")
forecast_lengths = [len(record["data"]) for record in records]
forecast_counts = Counter(forecast_lengths)

lengths = sorted(forecast_counts.keys())
counts = [forecast_counts[l] for l in lengths]

max_forecast_count = max(counts)

width3, height3 = 800, 500
padding3 = 80
plot_width3 = width3 - 2*padding3
plot_height3 = height3 - 2*padding3
bar_width3 = plot_width3 / len(lengths) * 0.7

svg3 = f'''<svg width="{width3}" height="{height3}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .grid {{ stroke: #ddd; }}
    .axis {{ stroke: black; stroke-width: 2; }}
    .bar {{ fill: steelblue; stroke: black; stroke-width: 0.5; }}
    .grid-text {{ font-size: 11px; text-anchor: middle; }}
    .title {{ font-size: 18px; font-weight: bold; text-anchor: middle; }}
    .label {{ font-size: 14px; font-weight: bold; }}
    .value-text {{ font-size: 12px; font-weight: bold; text-anchor: middle; }}
  </style>

  <!-- Title -->
  <text x="{width3/2}" y="30" class="title">Distribution of Forecast Lengths (n={len(records):,} cities)</text>

  <!-- Y-axis label -->
  <text x="20" y="{height3/2}" text-anchor="middle" transform="rotate(-90 20 {height3/2})" class="label">Number of Cities</text>

  <!-- X-axis label -->
  <text x="{width3/2}" y="{height3-10}" text-anchor="middle" class="label">Forecast Length (number of days)</text>

  <!-- Axes -->
  <line x1="{padding3}" y1="{padding3}" x2="{padding3}" y2="{padding3+plot_height3}" class="axis"/>
  <line x1="{padding3}" y1="{padding3+plot_height3}" x2="{padding3+plot_width3}" y2="{padding3+plot_height3}" class="axis"/>
'''

# Add grid lines
for i in range(6):
    y = padding3 + plot_height3 - (i / 5) * plot_height3
    svg3 += f'  <line x1="{padding3}" y1="{y}" x2="{padding3+plot_width3}" y2="{y}" class="grid" stroke-dasharray="2,2"/>\n'
    count_label = int(i / 5 * max_forecast_count)
    svg3 += f'  <text x="{padding3-10}" y="{y+4}" text-anchor="end" class="grid-text">{count_label:,}</text>\n'

# Add bars
for i, (length, count) in enumerate(zip(lengths, counts)):
    x = padding3 + (i / len(lengths)) * plot_width3 + (plot_width3 / len(lengths) - bar_width3) / 2
    bar_height = (count / max_forecast_count) * plot_height3 if max_forecast_count > 0 else 0
    y = padding3 + plot_height3 - bar_height
    svg3 += f'  <rect x="{x}" y="{y}" width="{bar_width3}" height="{bar_height}" class="bar"/>\n'

    # Add value label on top of bar
    svg3 += f'  <text x="{x + bar_width3/2}" y="{y-5}" class="value-text">{count:,}</text>\n'

    # Add x-axis label
    x_label = x + bar_width3 / 2
    svg3 += f'  <text x="{x_label}" y="{padding3+plot_height3+20}" class="grid-text">{length}</text>\n'

svg3 += '</svg>'

with open('plot_3_forecast_length_distribution.svg', 'w') as f:
    f.write(svg3)
print("✓ Chart 3 saved: plot_3_forecast_length_distribution.svg")

print("\n" + "=" * 60)
print("All charts created successfully!")
print("=" * 60)
print(f"Summary:")
print(f"  Chart 1: San Francisco temperature range ({len(sf_temps_min)} days)")
print(f"           Min: {min(sf_temps_min):.2f}°C, Max: {max(sf_temps_max):.2f}°C")
print(f"  Chart 2: {len(all_temps_day):,} total forecast days across all cities")
print(f"           Mean temperature: {mean_temp:.2f}°C")
print(f"           Range: {min_temp_all:.2f}°C to {max_temp_all:.2f}°C")
print(f"  Chart 3: {len(records):,} cities with forecast lengths: {dict(sorted(forecast_counts.items()))}")
