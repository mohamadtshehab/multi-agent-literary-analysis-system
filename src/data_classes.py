from dataclasses import dataclass


@dataclass
class Profile:
    name: str
    age: int
    role: str
    physical_characteristics: str
    personality: str
    events: list[str]
    relationships: list[str]