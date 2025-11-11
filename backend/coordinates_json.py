import json
import os

coordinates = [
    {
        "Unit": {
            "1": [0, 0],
            "2": [0, 0],
            "3": [0, 0],
            "4": [0, 0],
            "5": [0, 0],
            "6": [0, 0]
        }
    }
]
def saveToJson(index, x, y):
    try:
        if os.path.exists("coordinates.json"):
            with open("coordinates.json", "r") as file:
                data = json.load(file)
        else:
            data = coordinates.copy()
        
        
        key = str(index + 1)
        
        if len(data) > 0 and "Unit" in data[0]:
            data[0]["Unit"][key] = [x, y]
        else:
            data = coordinates.copy()
            data[0]["Unit"][key] = [x,y]
        with open("coordinates.json", "w") as file:
            json.dump(data, file, indent=2)
            
        print(f"Saved coordinates as {x}, {y} in {data[0]['Unit'][key]}")
    
    except Exception as e:
        print(f"Error JSON: {e}")
        
def loadFromJson():
    try:
        if os.path.exists("coordinates.json"):
            with open("coordinates.json", "r") as file:
                return json.load(file)
        else:
            return coordinates.copy()
    except Exception as e:
        print(f"Failed to load JSON: {e}")