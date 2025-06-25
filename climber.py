from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from climbersapp import Expedition


class Climber:
    """
    Represents a climber who participated in an expedition.

    Attributes:
        id (int): Unique identifier for the climber.
        first_name (str): Climber's first name.
        last_name (str): Climber's last name.
        nationality (str): Country of origin.
        date_of_birth (date): Date the climber was born.
        expedition_id (int): ID of the expedition they participated in.
    """

    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        nationality: str,
        date_of_birth: date,
        expedition_id: int,
    ) -> None:
        """
        Initializes a Climber object with personal and expedition information.

        Args:
            id (int): Unique ID of the climber.
            first_name (str): First name.
            last_name (str): Last name.
            nationality (str): Country of origin.
            date_of_birth (date): Date of birth.
            expedition_id (int): Linked expedition's ID.
        """
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.nationality = nationality
        self.date_of_birth = date_of_birth
        self.expedition_id = expedition_id

    def __repr__(self) -> str:
        """
        Returns a string representation of the Climber object.
        This helps for debugging or logging.
        """
        return (
            f"Climber(date_of_birth={self.date_of_birth}, expedition_id={self.expedition_id}, "
            f"first_name={self.first_name}, id={self.id}, last_name={self.last_name}, "
            f"nationality={self.nationality})"
        )

    def get_age(self, at_date: date = date.today()) -> int:
        """
        Calculates the climber's age on a given date.

        Args:
            at_date (date): The reference date to calculate age from. Defaults to today's date.

        Returns:
            int: Age of the climber at the specified date.
        """
        return (
            at_date.year
            - self.date_of_birth.year
            - (
                (at_date.month, at_date.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )

    def is_same_climber(self, climber: "Climber") -> bool:
        """
        Checks if the current climber matches another climber's identity (not using ID).

        Args:
            climber (Climber): Another climber object to compare with.

        Returns:
            bool: True if names, nationality, and birthdate match. False otherwise.
        """
        return (
            self.first_name == climber.first_name
            and self.last_name == climber.last_name
            and self.date_of_birth == climber.date_of_birth
            and self.nationality == climber.nationality
        )

    def get_expedition(self) -> "Expedition":
        """
        Retrieves the Expedition object associated with this climber.

        Returns:
            Expedition: The expedition the climber was part of.
        """
        from climbersapp import (
            get_expedition_by_id,
        )  # Delayed import to avoid circular imports

        return get_expedition_by_id(self.expedition_id)
