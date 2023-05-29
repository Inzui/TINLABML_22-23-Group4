import json

class CarStateDto():
    def __init__(self, carStateDict):
        for key in carStateDict:
            setattr(self, key, carStateDict[key])
    
    def __str__(self):
        outputString = ""
        for attr, value in self.__dict__.items():
            outputString += f"{attr, value}\n"
        return outputString
    
    def getDict(self):
        return self.__dict__
    
    def getJSON(self):
        return json.dumps(self.__dict__)