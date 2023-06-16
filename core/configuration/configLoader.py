import json



def loadConfig(file):
    file = open(file+".json", "r")
    return json.load(file)

current_config = loadConfig("C:\\Users\\hans\\PycharmProjects\\LegoRobot\\core\\configuration\\verynice")


print(current_config)



def saveConfig(file, config):
    jsonObject = json.dumps(config, indent=4)

    file = open(file+".json", "w")

    file.write(jsonObject)
