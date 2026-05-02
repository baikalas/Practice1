import json
import os

FILE = "leaderboard.json"

def load():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save(name, score, distance):
    data = load()
    data.append({
        "name": name,
        "score": score,
        "distance": distance
    })

    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)