import unittest
from datetime import datetime
from climber import Climber
from expedition import Expedition
from mountain import Mountain
from climbersreporter import Reporter


class TestReporter(unittest.TestCase):
    """Unit tests for the Reporter class."""

    def setUp(self) -> None:
        # This method runs before every test to create a Reporter instance
        self.reporter = Reporter()

    def test_total_amount_of_climbers(self) -> None:
        # Test if total climbers is an integer and not negative
        result = self.reporter.total_amount_of_climbers()
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)

    def test_total_amount_of_unique_climbers(self) -> None:
        # Test if unique climber count is an integer and valid
        result = self.reporter.total_amount_of_unique_climbers()
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)

    def test_highest_mountain(self) -> None:
        # Test if highest mountain is valid and has height above 8000m
        mountain = self.reporter.highest_mountain()
        self.assertIsNotNone(mountain)
        self.assertIsInstance(mountain, Mountain)
        self.assertGreater(mountain.height, 8000)
        self.assertTrue(mountain.name)

    def test_longest_and_shortest_expedition(self) -> None:
        # Test if longest and shortest expeditions are valid and logical
        longest, shortest = self.reporter.longest_and_shortest_expedition()
        self.assertIsInstance(longest, Expedition)
        self.assertIsInstance(shortest, Expedition)
        self.assertGreaterEqual(longest.duration, shortest.duration)
        self.assertGreaterEqual(longest.duration, 0)

    def test_expedition_with_most_climbers(self) -> None:
        # Test if the expedition with the most climbers exists and is valid
        expedition = self.reporter.expedition_with_most_climbers()
        self.assertIsNotNone(expedition)
        self.assertIsInstance(expedition, Expedition)
        self.assertGreater(expedition.duration, 0)

    def test_mountain_with_most_expeditions(self) -> None:
        # Test if the mountain with the most expeditions is returned
        mountain = self.reporter.mountain_with_most_expeditions()
        self.assertIsNotNone(mountain)
        self.assertIsInstance(mountain, Mountain)
        self.assertTrue(mountain.name)

    def test_get_first_expedition(self) -> None:
        # Test if the first expedition is from before the year 2000
        expedition = self.reporter.get_first_expedition()
        self.assertIsNotNone(expedition)
        self.assertIsInstance(expedition, Expedition)
        self.assertLess(expedition.date.year, 2000)

    def test_get_first_successful_expedition(self) -> None:
        # Test if the first successful expedition is returned
        expedition = self.reporter.get_first_expedition(only_succesful=True)
        self.assertIsNotNone(expedition)
        self.assertIsInstance(expedition, Expedition)
        self.assertTrue(expedition.success)

    def test_get_latest_expedition(self) -> None:
        # Test if the latest expedition is from the 2000s or later
        expedition = self.reporter.get_latest_expedition()
        self.assertIsNotNone(expedition)
        self.assertIsInstance(expedition, Expedition)
        self.assertGreaterEqual(expedition.date.year, 2000)

    def test_get_latest_successful_expedition(self) -> None:
        # Test if the latest successful expedition is valid
        expedition = self.reporter.get_latest_expedition(only_succesful=True)
        self.assertIsNotNone(expedition)
        self.assertIsInstance(expedition, Expedition)
        self.assertTrue(expedition.success)

    def test_expedition_date_formatting(self) -> None:
        # Test if the expedition date is formatted as DD/MM/YYYY
        expedition = self.reporter.get_first_expedition()
        formatted = expedition.convert_date("%d/%m/%Y")
        self.assertRegex(formatted, r"\d{2}/\d{2}/\d{4}")

    def test_expedition_duration_formatting(self) -> None:
        # Test if the expedition duration is formatted correctly
        expedition = self.reporter.get_latest_expedition()
        formatted = expedition.convert_duration("%D days, %H hours, %M minutes")
        self.assertRegex(formatted, r"\d{2} days, \d{2} hours, \d{2} minutes")

    def test_get_climbers_that_climbed_mountain_between(self) -> None:
        # Test if climbers between dates are returned correctly
        mountain = Mountain(
            33, "Molamenqing", "China", 7703, 433, range_="Langtang Himalaya"
        )
        start = datetime(1990, 1, 1)
        end = datetime(1995, 1, 1)
        climbers = self.reporter.get_climbers_that_climbed_mountain_between(
            mountain, start, end
        )
        self.assertIsInstance(climbers, tuple)
        for climber in climbers:
            self.assertIsInstance(climber, Climber)
            self.assertGreater(climber.expedition_id, 0)

    def test_get_climbers_that_climbed_mountain_between_empty(self) -> None:
        # Test with a date range that returns no climbers
        mountain = Mountain(
            33, "Molamenqing", "China", 7703, 433, range_="Langtang Himalaya"
        )
        start = datetime(1800, 1, 1)
        end = datetime(1800, 12, 31)
        climbers = self.reporter.get_climbers_that_climbed_mountain_between(
            mountain, start, end
        )
        self.assertEqual(climbers, ())

    def test_get_mountains_in_country(self) -> None:
        # Test if mountains in a valid country (Nepal) are returned
        mountains = self.reporter.get_mountains_in_country("Nepal")
        self.assertIsInstance(mountains, tuple)
        for mountain in mountains:
            self.assertIsInstance(mountain, Mountain)
            self.assertEqual(mountain.country, "Nepal")

    def test_get_mountains_in_invalid_country(self) -> None:
        # Test if an invalid country returns an empty result
        mountains = self.reporter.get_mountains_in_country("Atlantis")
        self.assertEqual(mountains, ())

    def test_get_climbers_from_country(self) -> None:
        # Test if climbers from a valid country are returned
        climbers = self.reporter.get_climbers_from_country("Sweden")
        self.assertIsInstance(climbers, tuple)
        for climber in climbers:
            self.assertIsInstance(climber, Climber)
            self.assertEqual(climber.nationality, "Sweden")

    def test_get_climbers_from_invalid_country(self) -> None:
        # Test if an invalid country returns no climbers
        climbers = self.reporter.get_climbers_from_country("Narnia")
        self.assertEqual(climbers, ())

    def test_empty_first_expedition_handling(self) -> None:
        # Test if get_first_expedition returns None or Expedition safely
        expedition = self.reporter.get_first_expedition()
        self.assertTrue(expedition is None or isinstance(expedition, Expedition))

    def test_empty_highest_mountain_handling(self) -> None:
        # Test if highest_mountain returns None or valid Mountain
        mountain = self.reporter.highest_mountain()
        self.assertTrue(mountain is None or isinstance(mountain, Mountain))


if __name__ == "__main__":
    unittest.main()
