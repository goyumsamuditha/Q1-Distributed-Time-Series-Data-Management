// Anomaly Isolation Filters: Captures observations exceeding two standard deviations from dataset mean
data = from(bucket: "weather_raw")
  |> range(start: 2006-01-01T00:00:00Z, stop: 2006-12-31T23:59:59Z)
  |> filter(fn: (r) => r["_measurement"] == "weather_observations")
  |> filter(fn: (r) => r["_field"] == "temperature")

meanVal = data |> mean() |> findRecord(fn: (key) => true, idx: 0)._value
stdDevVal = data |> stddev() |> findRecord(fn: (key) => true, idx: 0)._value

upperBound = meanVal + (2.0 * stdDevVal)
lowerBound = meanVal - (2.0 * stdDevVal)

data
  |> filter(fn: (r) => r._value > upperBound or r._value < lowerBound)
  |> yield(name: "temperature_anomalies_2sigma")