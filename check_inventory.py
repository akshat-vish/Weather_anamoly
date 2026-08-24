import meteostat as ms

stations = [
    "42182",  # New Delhi / Safdarjung
    "42181",  # New Delhi / Palam
    "42139",  # Meerut
    "42176",  # Rohtak
    "42262",  # Aligarh
    "42137",  # Karnal
    "42140",  # Roorkee
]

for station_id in stations:

    print("\n" + "=" * 60)
    print("STATION:", station_id)

    inventory = ms.stations.inventory(station_id)

    print("Available from:", inventory.start)
    print("Available until:", inventory.end)
    print("Parameters:", inventory.parameters)