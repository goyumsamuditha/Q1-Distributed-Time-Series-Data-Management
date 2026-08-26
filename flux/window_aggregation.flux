data = from(bucket: "weather_bucket")
  |> range(start: 2006-01-01T00:00:00Z, stop: 2006-12-31T23:59:59Z)
  |> filter(fn: (r) => r["_measurement"] == "weather_observations")
  |> filter(fn: (r) => r["_field"] == "temperature")

// Save the record first, then extract the value to satisfy the Flux parser
meanRecord = data |> mean() |> findRecord(fn: (key) => true, idx: 0)
stdDevRecord = data |> stddev() |> findRecord(fn: (key) => true, idx: 0)

upperBound = meanRecord._value + (2.0 * stdDevRecord._value)
lowerBound = meanRecord._value - (2.0 * stdDevRecord._value)

data
  |> filter(fn: (r) => r._value > upperBound or r._value < lowerBound)
  |> yield(name: "temperature_anomalies_2sigma")