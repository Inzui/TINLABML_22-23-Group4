import math

DEGREE_PER_RADIANS = 180 / math.pi
MPS_PER_KMH = 1000 / 3600

class Command():
    def __init__(self):
        self.accelerator = 0.0
        self.brake = 0.0
        self.gear = 0
        self.steering = 0.0
        self.focus = 0.0

    @property
    def actuator_dict(self):
        return dict(
            accel=[self.accelerator],
            brake=[self.brake],
            gear=[self.gear],
            steer=[self.steering],
            clutch=[0],  # server car does not need clutch control?
            focus=[self.focus],
            meta=[0]  # no support for server restart via meta=1
        )
