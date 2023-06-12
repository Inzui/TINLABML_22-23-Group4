class MemoryService():
    @staticmethod
    def loadFastestLapTime(path: str) -> float:
        try:
            f = open(path, "r")
            return float(f.read())
        except:
            return 10000.0

    @staticmethod
    def writeFastestlapTime(path: str, lapTime: float):
        f = open(path, "w")
        f.write(str(lapTime))
        f.close()