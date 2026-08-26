// Downsampling Task: Continuously summarizes historical data into auxiliary 30-day retention bucket
from(bucket: "weather_bucket")
    |> range(start: -2h)
    |> filter(fn: (r) => r["_measurement"] == "weather_observations")
    |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
    |> to(bucket: "weather_downsampled", org: "weather_org")
