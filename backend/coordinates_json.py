import json

coordinates = [
    {
        "Unit": {
            "Unit_1": (0, 0),
            "Unit_2": (0, 0),
            "Unit_3": (0, 0),
            "Unit_4": (0, 0),
            "Unit_5": (0, 0),
            "Unit_6": (0, 0)
        }
    }
]



unit_1_coord = (12, 12)

coordinates[0]["Unit"]["Unit_1"] = unit_1_coord

with open("coordinates.json", "w") as file:
    json.dump(coordinates, file, indent=2)