import json

def load_config(filepath="config.json"):
    with open(filepath, "r") as file:
        config = json.load(file)
    return config

### config.json
{
    "screen_width": 800,
    "screen_height": 600,
    "fps": 60
}
