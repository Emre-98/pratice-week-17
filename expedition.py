from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from climbersapp import Climber, Mountain


class Expedition:
    """
    Represents a climbing expedition, including details like the mountain climbed,
    duration, location, and whether it was successful.
    """

    def __init__(self, id, name, mountain_id, start, date, country, duration, success):
        """
        Initializes an Expedition object.

        Args:
            id (int): Unique identifier for the expedition.
            name (str): Name of the expedition.
            mountain_id (int): ID of the mountain that was climbed.
            start (str): Starting location of the expedition.
            date (str or datetime): Date of the expedition.
            country (str): Country where the expedition took place.
            duration (int): Duration of the expedition in minutes.
            success (bool or int): Whether the expedition was successful.
        """
        self.id = id
        self.name = name
        self.mountain_id = mountain_id
        self.start = start

        # Convert date string to datetime if needed
        self.date = (
            datetime.strptime(date, "%Y-%m-%d") if isinstance(date, str) else date
        )

        self.country = country
        self.duration = duration
        self.success = bool(success)

    def __repr__(self):
        """
        Returns a readable string representation of the expedition.
        """
        return (
            f"Expedition(country={self.country}, date={self.date.strftime('%Y-%m-%d')}, duration={self.duration}, "
            f"id={self.id}, mountain_id={self.mountain_id}, name={self.name}, start={self.start}, success={int(self.success)})"
        )

    def get_climbers(self) -> list["Climber"]:
        """
        Returns a list of climbers who were part of this expedition.

        Uses a helper function from climbersapp to fetch data.
        """
        from climbersapp import get_climbers_by_expedition_id

        return get_climbers_by_expedition_id(self.id)

    def get_mountain(self) -> "Mountain":
        """
        Returns the mountain object that this expedition targeted.

        Uses a helper function from climbersapp to fetch data.
        """
        from climbersapp import get_mountain_by_rank

        return get_mountain_by_rank(self.mountain_id)

    def convert_date(self, to_format: str) -> str:
        """
        Converts the expedition's date to a specific string format.

        Args:
            to_format (str): Desired format (e.g. "%d-%m-%Y")

        Returns:
            str: Formatted date string.
        """
        return self.date.strftime(to_format)

    def convert_duration(self, to_format: str) -> str:
        """
        Converts the duration in minutes to a formatted string using placeholders:
        %D = days, %H = hours, %M = minutes

        Args:
            to_format (str): Format string with placeholders (e.g. "%D days, %H hours, %M minutes")

        Returns:
            str: Formatted duration string.
        """
        # Calculate days, hours, and minutes from total minutes
        days = self.duration // (24 * 60)
        hours = (self.duration % (24 * 60)) // 60
        minutes = self.duration % 60

        # Replace placeholders with actual values
        result = to_format
        result = result.replace("%D", f"{days:02}")
        result = result.replace("%H", f"{hours:02}")
        result = result.replace("%M", f"{minutes:02}")
        return result


print("Expedition")