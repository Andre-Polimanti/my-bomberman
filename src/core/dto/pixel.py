from dataclasses import dataclass

@dataclass
class Pixel:
    obstructed: bool = False
    burning: bool = False