// Anomaly Isolation Filters: Captures observations exceeding two standard deviations from dataset mean
data = from(bucket: "weather_bucket")
      |> range(start: 2006-01-01T00:00:00Z, stop: 2006-12-31T23:59:59Z)
      |> filter(fn: (r) => r["_measurement"] == "weather_observations")
      |> filter(fn: (r) => r["_field"] == "temperature")

    meanRecord = data |> mean() |> findRecord(fn: (key) => true, idx: 0)
    stdDevRecord = data |> stddev() |> findRecord(fn: (key) => true, idx: 0)

    upperBound = meanRecord._value + (2.0 * stdDevRecord._value)
    lowerBound = meanRecord._value - (2.0 * stdDevRecord._value)

    data
      |> filter(fn: (r) => r._value > upperBound or r._value < lowerBound)
      |> limit(n: 5) // Limit to 5 for clean terminal output