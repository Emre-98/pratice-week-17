import os
import sys
import sqlite3
import csv
from datetime import datetime

from mountain import Mountain
from expedition import Expedition
from climber import Climber

# Set up connection to SQLite database



class Reporter:
    """
    This class provides various reporting features to extract and analyze
    information from the climbers, expeditions, and mountains database.
    """

    chimney = 5

    def initialize_database(self, db_path):
        connection = sqlite3.connect(db_path)
        self.cursor = connection.cursor()
            

    def total_amount_of_climbers(self) -> int:
        """Returns the total number of climbers in the database."""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM climbers")
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            print("Database error:", e)
            return 0

    def total_amount_of_unique_climbers(self) -> int:
        """Returns the total number of unique climbers based on identity fields."""
        try:
            self.cursor.execute(
                """
                SELECT COUNT(*) FROM (
                    SELECT DISTINCT first_name, last_name, nationality, date_of_birth FROM climbers
                )
                """
            )
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            print("Database error:", e)
            return 0

    def highest_mountain(self) -> Mountain:
        """Returns the highest mountain based on height."""
        self.cursor.execute(
            "SELECT country, height, name, prominence, range, rank FROM mountains ORDER BY height DESC LIMIT 1"
        )
        row = self.cursor.fetchone()
        if row:
            return Mountain(row[5], row[2], row[0], row[1], row[3], row[4])
        raise ValueError("No mountain data found in the database.")

    def longest_and_shortest_expedition(self) -> tuple[Expedition, Expedition]:
        """Returns the longest and shortest expeditions based on duration."""
        self.cursor.execute(
            "SELECT country, date, duration, id, mountain_id, name, start_location, success "
            "FROM expeditions ORDER BY duration DESC LIMIT 1"
        )
        row1 = self.cursor.fetchone()
        longest = Expedition(
            row1[3],
            row1[5],
            row1[4],
            row1[6],
            row1[1].split(" ")[0],
            row1[0],
            row1[2],
            row1[7],
        )

        self.cursor.execute(
            "SELECT country, date, duration, id, mountain_id, name, start_location, success "
            "FROM expeditions ORDER BY duration ASC LIMIT 1"
        )
        row2 = self.cursor.fetchone()
        shortest = Expedition(
            row2[3],
            row2[5],
            row2[4],
            row2[6],
            row2[1].split(" ")[0],
            row2[0],
            row2[2],
            row2[7],
        )

        return longest, shortest

    def expedition_with_most_climbers(self) -> Expedition:
        """Finds and returns the expedition with the most climbers."""
        self.cursor.execute(
            """
            SELECT expedition_id FROM climbers
            GROUP BY expedition_id
            ORDER BY COUNT(*) DESC
            LIMIT 1
            """
        )
        expedition_id = self.cursor.fetchone()[0]
        self.cursor.execute(
            "SELECT country, date, duration, id, mountain_id, name, start_location, success "
            "FROM expeditions WHERE id = ?",
            (expedition_id,),
        )
        row = self.cursor.fetchone()
        return Expedition(
            row[3], row[5], row[4], row[6], row[1].split(" ")[0], row[0], row[2], row[7]
        )

    def mountain_with_most_expeditions(self) -> Mountain:
        """Finds and returns the mountain with the most expeditions."""
        self.cursor.execute(
            """
            SELECT mountain_id FROM expeditions
            GROUP BY mountain_id
            ORDER BY COUNT(*) DESC
            LIMIT 1
            """
        )
        mountain_id = self.cursor.fetchone()[0]
        self.cursor.execute(
            "SELECT country, height, name, prominence, range, rank FROM mountains WHERE rank = ?",
            (mountain_id,),
        )
        row = self.cursor.fetchone()
        return Mountain(row[5], row[2], row[0], row[1], row[3], row[4])

    def get_first_expedition(self, only_succesful: bool = False) -> Expedition:
        """Returns the earliest expedition. Optionally filters only successful ones."""
        if only_succesful:
            self.cursor.execute(
                "SELECT country, date, duration, id, mountain_id, name, start_location, success "
                "FROM expeditions WHERE success = 1 ORDER BY date ASC LIMIT 1"
            )
        else:
            self.cursor.execute(
                "SELECT country, date, duration, id, mountain_id, name, start_location, success "
                "FROM expeditions ORDER BY date ASC LIMIT 1"
            )
        row = self.cursor.fetchone()
        return Expedition(
            row[3], row[5], row[4], row[6], row[1].split(" ")[0], row[0], row[2], row[7]
        )

    def get_latest_expedition(self, only_succesful: bool = False) -> Expedition:
        """Returns the most recent expedition. Optionally filters only successful ones."""
        if only_succesful:
            self.cursor.execute(
                "SELECT country, date, duration, id, mountain_id, name, start_location, success "
                "FROM expeditions WHERE success = 1 ORDER BY date DESC LIMIT 1"
            )
        else:
            self.cursor.execute(
                "SELECT country, date, duration, id, mountain_id, name, start_location, success "
                "FROM expeditions ORDER BY date DESC LIMIT 1"
            )
        row = self.cursor.fetchone()
        return Expedition(
            row[3], row[5], row[4], row[6], row[1].split(" ")[0], row[0], row[2], row[7]
        )

    def get_climbers_that_climbed_mountain_between(
        self,
        mountain: Mountain,
        start: datetime,
        end: datetime,
        to_csv: bool = False,
    ) -> tuple[Climber, ...]:
        """
        Get all climbers who climbed a specific mountain between two dates.
        Optionally writes the result to a CSV file.
        """
        self.cursor.execute(
            """
            SELECT c.* FROM climbers c
            JOIN expeditions e ON c.expedition_id = e.id
            WHERE e.mountain_id = ? AND e.date BETWEEN ? AND ?
            """,
            (mountain.rank, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")),
        )
        rows = self.cursor.fetchall()
        climbers = tuple(
            Climber(
                id=row[0],
                first_name=row[1],
                last_name=row[2],
                nationality=row[3],
                date_of_birth=(
                    datetime.strptime(row[4], "%Y-%m-%d").date()
                    if isinstance(row[4], str)
                    else row[4]
                ),
                expedition_id=row[5],
            )
            for row in rows
        )

        if to_csv:
            filename = (
                f"Climbers mountain {mountain.name} between "
                f"{start.strftime('%Y-%m-%d')} and {end.strftime('%Y-%m-%d')}.csv"
            )
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "id",
                        "first_name",
                        "last_name",
                        "nationality",
                        "date_of_birth",
                        "expedition_id",
                    ]
                )
                for c in climbers:
                    writer.writerow(
                        [
                            c.id,
                            c.first_name,
                            c.last_name,
                            c.nationality,
                            c.date_of_birth.strftime("%Y-%m-%d"),
                            c.expedition_id,
                        ]
                    )

        return climbers

    def get_mountains_in_country(
        self, country: str, to_csv: bool = False
    ) -> tuple[Mountain, ...]:
        """Returns all mountains in the specified country. Optionally writes to CSV."""
        self.cursor.execute(
            "SELECT country, height, name, prominence, range, rank FROM mountains WHERE LOWER(country) = LOWER(?)",
            (country,),
        )
        rows = self.cursor.fetchall()
        mountains = tuple(
            Mountain(row[5], row[2], row[0], row[1], row[3], row[4]) for row in rows
        )

        if to_csv:
            filename = f"Mountains in country {country}.csv"
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["rank", "name", "country", "height", "prominence", "range"]
                )
                for m in mountains:
                    writer.writerow(
                        [
                            m.rank,
                            m.name,
                            m.country,
                            m.height,
                            m.prominence,
                            m.range,
                        ]
                    )

        return mountains

    def get_climbers_from_country(
        self, country: str, to_csv: bool = False
    ) -> tuple[Climber, ...]:
        """Returns all climbers from the given country. Optionally writes to CSV."""
        self.cursor.execute(
            "SELECT * FROM climbers WHERE LOWER(nationality) = LOWER(?)", (country,)
        )
        rows = self.cursor.fetchall()
        climbers = tuple(
            Climber(
                id=row[0],
                first_name=row[1],
                last_name=row[2],
                nationality=row[3],
                date_of_birth=(
                    datetime.strptime(row[4], "%Y-%m-%d").date()
                    if isinstance(row[4], str)
                    else row[4]
                ),
                expedition_id=row[5],
            )
            for row in rows
        )

        if to_csv:
            filename = f"Climbers in country {country.capitalize()}.csv"
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "id",
                        "first_name",
                        "last_name",
                        "nationality",
                        "date_of_birth",
                        "expedition_id",
                    ]
                )
                for c in climbers:
                    writer.writerow(
                        [
                            c.id,
                            c.first_name,
                            c.last_name,
                            c.nationality,
                            c.date_of_birth.strftime("%Y-%m-%d"),
                            c.expedition_id,
                        ]
                    )

        return climbers


if __name__ == "__main__":
    noctibuttsdb_query = Reporter()
    climbersdb_query = Reporter()
    climbersapp_db_path = os.path.join(sys.path[0], "climbersapp.db")


    noctibutts_db_path = os.path.join(sys.path[0], "noctibuttsapp.db")
    noctibuttsdb_query.initialize_database(noctibutts_db_path)
    climbersdb_query.initialize_database(climbersapp_db_path)
    climbersdb_query.get_climbers_from_country("Sweden", to_csv=True)
    print(climbersdb_query.chimney)
    molamenqing = Mountain(
        rank=33,
        name="Molamenqing",
        country="China",
        height=7703,
        prominence=433,
        range_="Langtang Himalaya",
    )
    print(molamenqing.height)
    climbersdb_query.get_climbers_that_climbed_mountain_between(
        
        molamenqing,
        datetime.strptime("1990-01-01", "%Y-%m-%d"),
        datetime.strptime("1995-01-01", "%Y-%m-%d"),
        to_csv=True,
    )

    print("Total climbers:", climbersdb_query.total_amount_of_climbers())
    print("Highest mountain:", climbersdb_query.highest_mountain())
    print("Longest and shortest expedition:", climbersdb_query.longest_and_shortest_expedition())
    print("Expedition with most climbers:", climbersdb_query.expedition_with_most_climbers())
    print("Mountain with most expeditions:", climbersdb_query.mountain_with_most_expeditions())
    print("First expedition:", climbersdb_query.get_first_expedition())
    print("First successful expedition:", climbersdb_query.get_first_expedition(True))
    print("Latest expedition:", climbersdb_query.get_latest_expedition())
    print("Latest successful expedition:", climbersdb_query.get_latest_expedition(True))
