# weatherwrangle

Data-wrangling exercise on an OpenWeatherMap-style daily forecast dump (`daily_14.json`, NDJSON, one city per line, ~22.6k cities, forecasts for 2017-03-13 to 2017-03-29).

## Questions

See [questions.md](questions.md): record and country counts, top countries, exploding forecasts into one row per city/date, hottest cities by mean temperature, and a tidy table for San Francisco, CA.

## Files

| File | Purpose |
|---|---|
| `answers.py` | Answers all six questions, cross-checking each with two methods |
| `answer.txt` | Output of `answers.py` |
| `plot.py` | Generates the three SVG charts |
| `plot_*.svg` | SF temperature range, temp.day histogram, forecast-length distribution |

## Run

Standard library only (Python 3). Place `daily_14.json` in this folder (it's not committed, at 98 MB), then:

```bash
python3 answers.py > answer.txt
python3 plot.py
```

## Notes

- Temperatures are converted from Kelvin to °C, and dates are UTC (YYYY-MM-DD).
- Cities are identified by `city.id`, because names repeat. San Francisco, CA is id 5391959.
- Humidity is 0 in about 82% of rows, which is treated as missing.
- Cities have either 16 or 17 forecast days.
