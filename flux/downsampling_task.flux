// Downsampling Task: Continuously summarizes historical data into auxiliary 30-day retention bucket
option task = {
    name: "hourly_weather_downsampler",
    every: 1h,
}

from(bucket: "weather_raw")
    |> range(start: -2h)
    |> filter(fn: (r) => r["_measurement"] == "weather_observations")
    |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
    |> to(bucket: "weather_downsampled", org: "weather_org")