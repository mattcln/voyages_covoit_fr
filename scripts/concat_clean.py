import os
import time

import pandas as pd

in_relative_path = "../voyages_covoit_fr/exports_covoit/"
in_absolute_path = os.path.abspath(os.path.join(os.getcwd(), in_relative_path))
out_relative_path = "../voyages_covoit_fr/outputs/reduced_concat_covoit.csv"
out_absolute_path = os.path.abspath(os.path.join(os.getcwd(), out_relative_path))

colonne_a_garder = [
    "journey_id",
    "trip_id",
    "journey_start_datetime",
    "journey_start_insee",
    "journey_start_town",
    "journey_end_insee",
    "journey_end_town",
    "passenger_seats",
    "journey_distance",
    "journey_duration",
]


def clean_file(df: pd.DataFrame) -> pd.DataFrame:
    """_summary_

    :param df: _description_
    :return: _description_
    """


def concat_files() -> pd.DataFrame:
    df = pd.DataFrame()
    for files in os.listdir(in_absolute_path):
        print(f"Path : {in_absolute_path}/{files}")
        df_unique = pd.read_csv(f"{in_absolute_path}/{files}", sep=";", engine="python")
        df = pd.concat([df, df_unique])
        print(df.shape)


concat_files()
