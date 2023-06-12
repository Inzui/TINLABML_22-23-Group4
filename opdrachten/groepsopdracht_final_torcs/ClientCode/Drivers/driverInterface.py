from Dto.commandDto import CommandDto

class DriverInterface():
    def __init__(self) -> None:
        self.trainingSetPath = None

    def start(self):
        pass

    def train(self):
        pass

    def drive(self, carState: dict) -> CommandDto:
        pass