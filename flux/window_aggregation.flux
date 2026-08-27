from(bucket: "weather_bucket")
      |> range(start: 2006-01-01T00:00:00Z, stop: 2006-12-31T23:59:59Z)
      |> filter(fn: (r) => r["_measurement"] == "weather_observations")
      |> filter(fn: (r) => r["_field"] == "temperature")
      |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
      |> limit(n: 5) // Limit to 5 for clean terminal output