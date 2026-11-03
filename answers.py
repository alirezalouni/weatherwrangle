import json

# Q1: How many city records are in the file?
# This question asks: count the total number of top-level records (one per city) in the NDJSON file.

print("=" * 60)
print("Q1: How many city records are in the file?")
print("=" * 60)

# Method 1: Plain Python - count lines in a for loop
count_loop = 0
with open("daily_14.json") as f:
    for line in f:
        if line.strip():  # skip empty lines if any
            count_loop += 1

print(f"Method 1 (for loop with line count): {count_loop}")

# Method 2: Plain Python - list comprehension with json.loads
with open("daily_14.json") as f:
    records = [json.loads(line) for line in f if line.strip()]
count_json = len(records)

print(f"Method 2 (list comprehension with json.loads): {count_json}")

# Assert they match
assert count_loop == count_json, f"Methods disagree: {count_loop} vs {count_json}"
print(f"\n✓ Both methods agree: {count_loop} city records")

# Q2: How many unique countries are represented?
# This question asks: count the number of distinct country codes across all city records.

print("\n" + "=" * 60)
print("Q2: How many unique countries are represented?")
print("=" * 60)

# Method 1: Plain Python - use a set
countries_set = set()
empty_countries = []
with open("daily_14.json") as f:
    for line in f:
        record = json.loads(line)
        country = record["city"]["country"]
        if not country or not country.strip():
            empty_countries.append(record["city"])
        countries_set.add(country)

count_python_q2 = len(countries_set)
print(f"Method 1 (Plain Python - set): {count_python_q2}")

# Method 2: Plain Python - load all records and use set comprehension
with open("daily_14.json") as f:
    all_records = [json.loads(line) for line in f if line.strip()]

countries_set2 = {r["city"]["country"] for r in all_records}
count_python_q2_v2 = len(countries_set2)
print(f"Method 2 (Plain Python - set comprehension): {count_python_q2_v2}")

# Assert they match
assert count_python_q2 == count_python_q2_v2, f"Methods disagree: {count_python_q2} vs {count_python_q2_v2}"
print(f"\n✓ Both methods agree: {count_python_q2} unique countries")

# Print any empty country values
if empty_countries:
    print(f"\nWarning: Found {len(empty_countries)} records with empty country:")
    for rec in empty_countries:
        print(f"  - city_id={rec['id']}, name='{rec['name']}'")
else:
    print("\nNo empty country values found.")

# Q3: Which 10 countries have the most cities in this file?
# This question asks: rank countries by the count of unique city.ids in each country and list the top 10.

print("\n" + "=" * 60)
print("Q3: Which 10 countries have the most cities in this file?")
print("=" * 60)

# Method 1: Plain Python - use a dictionary with sets to group city.ids by country
from collections import defaultdict

country_city_ids_m1 = defaultdict(set)
with open("daily_14.json") as f:
    for line in f:
        record = json.loads(line)
        country = record["city"]["country"]
        city_id = record["city"]["id"]
        country_city_ids_m1[country].add(city_id)

# Count unique cities per country
city_counts_m1 = {country: len(city_ids) for country, city_ids in country_city_ids_m1.items()}
top_10_m1 = sorted(city_counts_m1.items(), key=lambda x: x[1], reverse=True)[:10]

print("Method 1 (dictionary with sets):")
for rank, (country, count) in enumerate(top_10_m1, 1):
    print(f"  {rank:2d}. {country}: {count:5d} cities")

# Method 2: Plain Python - load all records first, then group
country_city_ids_m2 = defaultdict(set)
for record in all_records:
    country = record["city"]["country"]
    city_id = record["city"]["id"]
    country_city_ids_m2[country].add(city_id)

# Count unique cities per country
city_counts_m2 = {country: len(city_ids) for country, city_ids in country_city_ids_m2.items()}
top_10_m2 = sorted(city_counts_m2.items(), key=lambda x: x[1], reverse=True)[:10]

print("\nMethod 2 (from pre-loaded records):")
for rank, (country, count) in enumerate(top_10_m2, 1):
    print(f"  {rank:2d}. {country}: {count:5d} cities")

# Assert they match
assert top_10_m1 == top_10_m2, f"Methods disagree!\nM1: {top_10_m1}\nM2: {top_10_m2}"
print("\n✓ Both methods agree")

# Q4: Explode each city's daily forecast array into one row per (city, country, date).
# This question asks: expand the nested data array so each forecast day becomes a separate row,
# then count the total number of rows.

print("\n" + "=" * 60)
print("Q4: Explode each city's daily forecast array into one row per (city, country, date).")
print("=" * 60)

# Method 1: Plain Python - iterate through records and build exploded rows
exploded_rows_m1 = []
data_length_sum = 0
with open("daily_14.json") as f:
    for line in f:
        record = json.loads(line)
        city_id = record["city"]["id"]
        city_name = record["city"]["name"]
        country = record["city"]["country"]

        for day_forecast in record["data"]:
            data_length_sum += 1
            row = {
                "city_id": city_id,
                "city_name": city_name,
                "country": country,
                "dt": day_forecast["dt"]
            }
            exploded_rows_m1.append(row)

count_m1 = len(exploded_rows_m1)
print(f"Method 1 (iterate and build rows): {count_m1:,} rows")
print(f"  Sum of all data array lengths: {data_length_sum:,}")

# Method 2: Plain Python - use list comprehension with nested loop
exploded_rows_m2 = [
    {
        "city_id": record["city"]["id"],
        "city_name": record["city"]["name"],
        "country": record["city"]["country"],
        "dt": day_forecast["dt"]
    }
    for record in all_records
    for day_forecast in record["data"]
]

count_m2 = len(exploded_rows_m2)
print(f"Method 2 (list comprehension with nested loop): {count_m2:,} rows")

# Assert both methods produce same count
assert count_m1 == count_m2, f"Methods disagree: {count_m1} vs {count_m2}"
print(f"\n✓ Both methods agree: {count_m1:,} total rows")

# Assert row count equals sum of all data array lengths
assert count_m1 == data_length_sum, f"Row count {count_m1} != sum of data lengths {data_length_sum}"
print(f"✓ Row count matches sum of data array lengths: {data_length_sum:,}")

# Q5: For each city, use the mean of temp.day across its forecast horizon and list the top 10 hottest cities.
# This question asks: group by city.id, calculate the mean of temp.day (in Celsius) for each city,
# then rank by mean temperature and show the top 10 hottest cities with their name, country, and mean temp.

print("\n" + "=" * 60)
print("Q5: Top 10 hottest cities by mean temp.day across forecast horizon")
print("=" * 60)

# Method 1: Plain Python - use dictionary to group and calculate means
city_temps_m1 = {}
with open("daily_14.json") as f:
    for line in f:
        record = json.loads(line)
        city_id = record["city"]["id"]
        city_name = record["city"]["name"]
        country = record["city"]["country"]

        # Calculate mean temp.day for this city (convert from Kelvin to Celsius)
        temps = [d["temp"]["day"] - 273.15 for d in record["data"]]
        mean_temp = sum(temps) / len(temps) if temps else 0

        city_temps_m1[city_id] = {
            "name": city_name,
            "country": country,
            "mean_temp_c": mean_temp
        }

# Sort by mean temperature (descending) and get top 10
top_10_m1 = sorted(
    city_temps_m1.items(),
    key=lambda x: x[1]["mean_temp_c"],
    reverse=True
)[:10]

print("Method 1 (iterate and calculate means):")
for rank, (city_id, data) in enumerate(top_10_m1, 1):
    print(f"  {rank:2d}. {data['name']:25s} ({data['country']})  {data['mean_temp_c']:6.2f}°C")

# Method 2: Plain Python - process pre-loaded records
city_temps_m2 = {}
for record in all_records:
    city_id = record["city"]["id"]
    city_name = record["city"]["name"]
    country = record["city"]["country"]

    # Calculate mean temp.day for this city (convert from Kelvin to Celsius)
    temps = [d["temp"]["day"] - 273.15 for d in record["data"]]
    mean_temp = sum(temps) / len(temps) if temps else 0

    city_temps_m2[city_id] = {
        "name": city_name,
        "country": country,
        "mean_temp_c": mean_temp
    }

# Sort by mean temperature (descending) and get top 10
top_10_m2 = sorted(
    city_temps_m2.items(),
    key=lambda x: x[1]["mean_temp_c"],
    reverse=True
)[:10]

print("\nMethod 2 (from pre-loaded records):")
for rank, (city_id, data) in enumerate(top_10_m2, 1):
    print(f"  {rank:2d}. {data['name']:25s} ({data['country']})  {data['mean_temp_c']:6.2f}°C")

# Assert both methods produce same top 10
assert top_10_m1 == top_10_m2, f"Methods disagree!"
print("\n✓ Both methods agree")

# Q6: Build a tidy table for San Francisco, California.
# This question asks: filter to San Francisco (city.id = 5391959), extract columns (date, temp_min, temp_max,
# humidity, weather_description), convert temperatures from Kelvin to Celsius, format dates as YYYY-MM-DD,
# treat humidity 0 as NaN, and show city name, country, and mean temp.day in Celsius.

print("\n" + "=" * 60)
print("Q6: Tidy table for San Francisco, California (city.id = 5391959)")
print("=" * 60)

import datetime

SF_CITY_ID = 5391959

# Method 1: Plain Python - find SF record and build rows
sf_rows_m1 = []
sf_city_info_m1 = {}
with open("daily_14.json") as f:
    for line in f:
        record = json.loads(line)
        if record["city"]["id"] == SF_CITY_ID:
            city_name = record["city"]["name"]
            country = record["city"]["country"]
            sf_city_info_m1 = {"name": city_name, "country": country}

            # Calculate mean temp.day
            temps_day = [d["temp"]["day"] - 273.15 for d in record["data"]]
            mean_temp_day = sum(temps_day) / len(temps_day) if temps_day else 0
            sf_city_info_m1["mean_temp_day_c"] = mean_temp_day

            for day in record["data"]:
                # Convert Unix timestamp to date
                dt_obj = datetime.datetime.utcfromtimestamp(day["dt"])
                date_str = dt_obj.strftime("%Y-%m-%d")

                # Extract temperatures (convert Kelvin to Celsius)
                temp_min_c = day["temp"]["min"] - 273.15
                temp_max_c = day["temp"]["max"] - 273.15

                # Treat humidity 0 as NaN
                humidity = day["humidity"]
                humidity = None if humidity == 0 else humidity

                # Extract weather description (first in list)
                weather_desc = day["weather"][0]["description"] if day["weather"] else ""

                row = {
                    "date": date_str,
                    "temp_min_c": temp_min_c,
                    "temp_max_c": temp_max_c,
                    "humidity": humidity,
                    "weather_description": weather_desc
                }
                sf_rows_m1.append(row)
            break

print(f"Method 1 (Plain Python - iterate and extract):")
print(f"  City: {sf_city_info_m1['name']}, {sf_city_info_m1['country']}")
print(f"  Mean temp (day): {sf_city_info_m1['mean_temp_day_c']:.2f}°C")
print(f"  Rows: {len(sf_rows_m1)}")
print("\n  Date         Temp Min (°C)  Temp Max (°C)  Humidity  Weather")
print("  " + "-" * 65)
for row in sf_rows_m1:
    hum_str = f"{row['humidity']:3d}%" if row['humidity'] is not None else "NaN"
    print(f"  {row['date']}      {row['temp_min_c']:6.2f}        {row['temp_max_c']:6.2f}       {hum_str:>4s}  {row['weather_description']}")

# Method 2: Plain Python - use pre-loaded records
sf_rows_m2 = []
sf_city_info_m2 = {}
for record in all_records:
    if record["city"]["id"] == SF_CITY_ID:
        city_name = record["city"]["name"]
        country = record["city"]["country"]
        sf_city_info_m2 = {"name": city_name, "country": country}

        # Calculate mean temp.day
        temps_day = [d["temp"]["day"] - 273.15 for d in record["data"]]
        mean_temp_day = sum(temps_day) / len(temps_day) if temps_day else 0
        sf_city_info_m2["mean_temp_day_c"] = mean_temp_day

        for day in record["data"]:
            # Convert Unix timestamp to date
            dt_obj = datetime.datetime.utcfromtimestamp(day["dt"])
            date_str = dt_obj.strftime("%Y-%m-%d")

            # Extract temperatures (convert Kelvin to Celsius)
            temp_min_c = day["temp"]["min"] - 273.15
            temp_max_c = day["temp"]["max"] - 273.15

            # Treat humidity 0 as NaN
            humidity = day["humidity"]
            humidity = None if humidity == 0 else humidity

            # Extract weather description (first in list)
            weather_desc = day["weather"][0]["description"] if day["weather"] else ""

            row = {
                "date": date_str,
                "temp_min_c": temp_min_c,
                "temp_max_c": temp_max_c,
                "humidity": humidity,
                "weather_description": weather_desc
            }
            sf_rows_m2.append(row)
        break

print(f"\nMethod 2 (Plain Python - from pre-loaded records):")
print(f"  City: {sf_city_info_m2['name']}, {sf_city_info_m2['country']}")
print(f"  Mean temp (day): {sf_city_info_m2['mean_temp_day_c']:.2f}°C")
print(f"  Rows: {len(sf_rows_m2)}")

# Assert both methods produce same rows and city info
assert len(sf_rows_m1) == len(sf_rows_m2), f"Row count mismatch: {len(sf_rows_m1)} vs {len(sf_rows_m2)}"
assert sf_rows_m1 == sf_rows_m2, "Row data mismatch"
assert sf_city_info_m1 == sf_city_info_m2, "City info mismatch"
print("\n✓ Both methods agree")
