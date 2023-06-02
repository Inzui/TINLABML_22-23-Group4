from Dto.carStateDto import CarStateDto
from Dto.commandDto import CommandDto

class DriverInterface():
    def drive(self, carState: dict) -> CommandDto:
        pass