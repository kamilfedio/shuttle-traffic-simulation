"""
Driver model
"""

from datetime import datetime


class Driver:
    def __init__(
        self,
        id: int,
        name: str,
        cereals_license: bool,
        reaction_time: float,
        arrived_time: float,
        left_time: float,
    ) -> None:
        self.id: int = id
        self.name: str = name
        self.cereals_license: bool = cereals_license
        self.reaction_time: float = reaction_time
        self.arrived_time: float = arrived_time
        self.left_time: float = left_time

    def __str__(self) -> str:
        return f"Driver {self.id} - {self.name}"
