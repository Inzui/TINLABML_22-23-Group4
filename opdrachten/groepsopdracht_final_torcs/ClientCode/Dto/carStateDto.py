class CarStateDto():
    def __init__(self, carStateDict):
        for key in carStateDict:
            setattr(self, key, carStateDict[key])
    
    def __str__(self):
        outputString = ""
        for attr, value in self.__dict__.items():
            outputString += f"{attr, value}\n"
        return outputString