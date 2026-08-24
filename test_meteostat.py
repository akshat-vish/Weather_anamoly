import meteostat as ms

# Delhi coordinates
POINT = ms.Point(28.6139, 77.2090)

# Find nearby stations
stations = ms.stations.nearby(
    POINT,
    radius=300000,
    limit=20
)

print("Stations found:")
print(stations)
