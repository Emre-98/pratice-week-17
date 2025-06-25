import os
import sys
import sqlite3
import json
from datetime import datetime

# Do NOT import Reporter or Mountain here to avoid circular imports
# Import them only inside __main__ or function scope if needed

# Get the absolute path to the database and JSON file
db_path = os.path.join(sys.path[0], "climbersapp.db")
json_path = os.path.join(sys.path[0], "expeditions.json")

# Connect to the SQLite database
connection = sqlite3.connect(db_path)
cursor = connection.cursor()


def is_database_empty():
    cursor.execute("SELECT COUNT(*) FROM climbers")
    return cursor.fetchone()[0] == 0


def load_json_and_insert():
    with open(json_path, "r", encoding="utf-8") as f:
        expeditions = json.load(f)

    for expedition in expeditions:
        m = expedition["mountain"]
        cursor.execute(
            "INSERT OR IGNORE INTO mountains (rank, name, country, height, prominence, range) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                m["rank"],
                m["name"],
                m["countries"][0],
                m["height"],
                m["prominence"],
                m["range"],
            ),
        )

        duration_str = expedition["duration"]
        h, m_ = map(int, duration_str.replace("H", ":").split(":"))
        duration_min = h * 60 + m_ #grabs duration from json and splits

        exp_date = datetime.strptime(expedition["date"], "%Y-%m-%d")
        cursor.execute(
            "INSERT INTO expeditions (id, name, mountain_id, start_location, date, country, duration, success) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                expedition["id"],
                expedition["name"],
                expedition["mountain"]["rank"],
                expedition["start"],
                exp_date.strftime("%Y-%m-%d"),
                expedition["country"],
                duration_min,
                int(expedition["success"]),
            ),
        )

        for climber in expedition["climbers"]:
            dob = datetime.strptime(climber["date_of_birth"], "%d-%m-%Y").strftime(
                "%Y-%m-%d"
            )
            cursor.execute(
                "INSERT INTO climbers (first_name, last_name, nationality, date_of_birth, expedition_id) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    climber["first_name"],
                    climber["last_name"],
                    climber["nationality"],
                    dob,
                    expedition["id"],
                ),
            )

    connection.commit()


def get_expedition_by_id(exp_id):
    cursor.execute("SELECT * FROM expeditions WHERE id = ?", (exp_id,))
    row = cursor.fetchone()
    if row:
        from expedition import Expedition

        return Expedition(*row)
    return None


def get_climbers_by_expedition_id(exp_id):
    cursor.execute("SELECT * FROM climbers WHERE expedition_id = ?", (exp_id,))
    rows = cursor.fetchall()
    from climber import Climber

    return [Climber(*row) for row in rows]


def get_mountain_by_rank(rank):
    cursor.execute("SELECT * FROM mountains WHERE rank = ?", (rank,))
    row = cursor.fetchone()
    if row:
        from mountain import Mountain

        return Mountain(
            rank=row[0],
            name=row[1],
            country=row[2],
            height=row[3],
            prominence=row[4],
            range_=row[5],
        )
    return None


def get_expeditions_by_mountain_rank(rank):
    cursor.execute("SELECT * FROM expeditions WHERE mountain_id = ?", (rank,))
    rows = cursor.fetchall()
    from expedition import Expedition

    return [Expedition(*row) for row in rows]


# === MAIN EXECUTION ===
if __name__ == "__main__":
    if is_database_empty():
        load_json_and_insert()

    # Delayed import to avoid circular import
    from climbersreporter import Reporter #take the blueprint from reporter
    from mountain import Mountain # Take the blueprint from mountain

    r = Reporter() #this creates the instance
    db_path = os.path.join(sys.path[0], "climbersapp.db")
    r.initialize_database(db_path)
    print("Total climbers:", r.total_amount_of_climbers())
    print("Highest mountain:", r.highest_mountain())
    print("Longest and shortest expedition:", r.longest_and_shortest_expedition())
    print("Expedition with most climbers:", r.expedition_with_most_climbers())
    print("Mountain with most expeditions:", r.mountain_with_most_expeditions())
    print("First expedition:", r.get_first_expedition())
    print("First successful expedition:", r.get_first_expedition(True))
    print("Latest expedition:", r.get_latest_expedition())
    print("Latest successful expedition:", r.get_latest_expedition(True))

    # Test Molamenqing filter
    mountain = Mountain( #instiating a mountain class. to get the f
        rank=33,
        name="Molamenqing",
        country="China",
        height=7703,
        prominence=433,
        range_="Langtang Himalaya",
    )
    print(
        r.get_climbers_that_climbed_mountain_between(
            mountain,
            datetime.strptime("1990-01-01", "%Y-%m-%d"),
            datetime.strptime("1995-01-01", "%Y-%m-%d"),
            False,
        )
    )

