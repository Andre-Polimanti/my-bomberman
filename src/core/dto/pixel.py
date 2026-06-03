from dataclasses import dataclass

@dataclass
class Pixel:
    obstructed: bool = False
    occupied: bool = False