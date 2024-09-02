import unittest
from datetime import datetime

import pandas as pd
from pandas.testing import assert_frame_equal

from scripts.concat_clean import clean_group_df, concat_clean_data


class TestConcatClean(unittest.TestCase):

    def test_clean_group_df_easy(self):
        input_data = {
            "journey_distance": [10, 20, 30, 40, 15, 25, 35, 45, 45, 45],
            "journey_duration": [20, 40, 60, 80, 30, 50, 70, 90, 90, 90],
            "passenger_seats": [1, 2, 3, 4, 1, 2, 3, 4, 1, 2],
            "journey_start_date": [
                datetime(2024, 9, 1),
                datetime(2024, 9, 1),
                datetime(2024, 9, 2),
                datetime(2024, 9, 2),
                datetime(2024, 9, 3),
                datetime(2024, 9, 3),
                datetime(2024, 9, 4),
                datetime(2024, 9, 4),
                datetime(2024, 9, 1),
                datetime(2024, 9, 2),
            ],
            "trip_id": [
                "trip_1",
                "trip_2",
                "trip_3",
                "trip_4",
                "trip_5",
                "trip_6",
                "trip_6",
                "trip_8",
                "trip_8",
                "trip_8",
            ],
        }
        input_df = pd.DataFrame(input_data)
        output_data = {
            "journey_start_date": [datetime(2024, 9, 1), datetime(2024, 9, 2), datetime(2024, 9, 3), datetime(2024, 9, 4)],
            "nb_passagers": [4, 9, 3, 7],
            "nb_trajets": [3, 3, 2, 2],
            "total_distance": [95, 340, 65, 285],
        }
        output_df = pd.DataFrame(output_data)
        assert_frame_equal(clean_group_df(input_df), output_df)

    def test_clean_group_df_checks_1(self):
        input_data = {
            "journey_distance": [10, 20, 30, 0, 0, 25, 400, 45, -45, 45],
            "journey_duration": [20, 0, 60, 80, 0, 50, -30, 90, 90, 90],
            "passenger_seats": [1, 2, 3, 4, 1, 2, 3, 4, 1, 2],
            "journey_start_date": [
                datetime(2024, 9, 1),
                datetime(2024, 9, 1),
                datetime(2024, 9, 2),
                datetime(2024, 9, 2),
                datetime(2024, 9, 3),
                datetime(2024, 9, 3),
                datetime(2024, 9, 4),
                datetime(2024, 9, 4),
                datetime(2024, 9, 1),
                datetime(2024, 9, 2),
            ],
            "trip_id": [
                "trip_1",
                "trip_2",
                "trip_3",
                "trip_4",
                "trip_5",
                "trip_6",
                "trip_6",
                "trip_8",
                "trip_8",
                "trip_8",
            ],
        }
        input_df = pd.DataFrame(input_data)
        output_data = {
            "journey_start_date": [datetime(2024, 9, 1), datetime(2024, 9, 2), datetime(2024, 9, 3), datetime(2024, 9, 4)],
            "nb_passagers": [4, 9, 2, 7],
            "nb_trajets": [3, 3, 1, 2],
            "total_distance": [5, 180, 50, 1380],
        }
        output_df = pd.DataFrame(output_data)
        assert_frame_equal(clean_group_df(input_df), output_df)

    def test_clean_group_df_checks_2(self):
        input_data = {
            "journey_distance": [10, 10, 20, 30, 40, 15],
            "journey_duration": [20, 20, 40, 60, 80, 30],
            "passenger_seats": [1, 2, 100, 3, 0, -10],
            "journey_start_date": [
                datetime(2024, 9, 1),
                datetime(2024, 9, 1),
                datetime(2024, 9, 1),
                datetime(2024, 9, 2),
                datetime(2024, 9, 2),
                datetime(2024, 9, 2),
            ],
            "trip_id": [
                "trip_1",
                "trip_2",
                "trip_3",
                "trip_4",
                "trip_5",
                "trip_6",
            ],
        }
        input_df = pd.DataFrame(input_data)
        output_data = {
            "journey_start_date": [datetime(2024, 9, 1), datetime(2024, 9, 2)],
            "nb_passagers": [3, 3],
            "nb_trajets": [2, 1],
            "total_distance": [30, 90],
        }
        output_df = pd.DataFrame(output_data)
        assert_frame_equal(clean_group_df(input_df), output_df)


if __name__ == "__main__":
    unittest.main()
