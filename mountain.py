from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from climbersapp import Expedition


class Mountain:
    """
    Represents a mountain, including its rank, name, country, height,
    prominence, and the range it belongs to.

    Attributes:
        rank (int): The mountain's ranking.
        name (str): Name of the mountain.
        country (str): Country where the mountain is located.
        height (int): Height of the mountain in meters.
        prominence (int): Prominence of the mountain in meters.
        range (str): Mountain range the mountain belongs to.
    """

    def __init__(
        self,
        rank: int,
        name: str,
        country: str,
        height: int,
        prominence: int,
        range: str = None,
        range_: str = None,
    ) -> None:
        """
        Initialize a Mountain object.

        Args:
            rank (int): The mountain's ranking.
            name (str): Name of the mountain.
            country (str): Country where the mountain is located.
            height (int): Height of the mountain in meters.
            prominence (int): Prominence of the mountain in meters.
            range (str, optional): Mountain range (if range_ not provided).
            range_ (str, optional): Alternative parameter for mountain range.
        """
        self.rank = rank
        self.name = name
        self.country = country
        self.height = height
        self.prominence = prominence
        self.range = range_ if range_ is not None else range

    def __repr__(self) -> str:
        """
        Returns a readable string showing the mountain's details.

        Returns:
            str: A formatted string with mountain details.
        """
        return (
            f"Mountain(country={self.country}, height={self.height}, name={self.name}, "
            f"prominence={self.prominence}, range={self.range}, rank={self.rank})"
        )

    def height_difference(self) -> int:
        """
        Calculates the difference between height and prominence.
        This tells how much of the mountain is above the lowest contour line.

        Returns:
            int: The height difference in meters.
        """
        return self.height - self.prominence

    def get_expeditions(self) -> list["Expedition"]:
        """
        Gets all expeditions that have taken place on this mountain.

        Returns:
            list[Expedition]: Expeditions linked to this mountain.
        """
        from climbersapp import (
            get_expeditions_by_mountain_rank,
        )  # Delayed import to avoid circular import

        return get_expeditions_by_mountain_rank(self.rank)

    def get_height_in_feet(self) -> float:
        """
        Converts the mountain's height from meters to feet.

        Returns:
            float: Height in feet (rounded to 2 decimals).
        """
        return round(self.height * 3.28084, 2)

    def get_prominence_in_feet(self) -> float:
        """
        Converts the mountain's prominence from meters to feet.

        Returns:
            float: Prominence in feet (rounded to 2 decimals).
        """
        return round(self.prominence * 3.28084, 2)
