import json


current_config = {
    "redLower": (10,10,10),
    "redUpper": (10, 40, 1)
}







def loadConfig(file):
    file = open(file+".json", "r")
    return json.load(file)

def saveConfig(file, config):
    jsonObject = json.dumps(config, indent=4)

    file = open(file+".json", "w")

    file.write(jsonObject)
