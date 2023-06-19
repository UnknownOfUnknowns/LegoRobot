import collections.abc
import json


def loadConfig(file):
    file = open(file + ".json", "r")
    data = json.load(file)

    formatted = {}
    for key, value in data.items():
        formatted[key] = tuple(value)
    return formatted


def loadConfigStandard(file):
    file = open(file + ".json", "r")
    return json.load(file)


current_config = loadConfig("/Users/ChristianKjeldgaardJensen/PycharmProjects/LegoRobot/core/configuration/robotCamConfigmonday")

robot_cam_config = loadConfigStandard(
    "/Users/ChristianKjeldgaardJensen/PycharmProjects/LegoRobot/core/configuration/robotCamConfig")

print(current_config)


def saveConfig(file, config):
    jsonObject = json.dumps(config, indent=4)

    file = open("/Users/ChristianKjeldgaardJensen/PycharmProjects/LegoRobot/core/configuration/robotCamConfig" + file + ".json", "w")

    file.write(jsonObject)
