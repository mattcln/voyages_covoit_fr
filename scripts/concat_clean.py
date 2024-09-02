import os
import time

import pandas as pd

in_relative_path = "../voyages_covoit_fr/exports_covoit/"
in_absolute_path = os.path.abspath(os.path.join(os.getcwd(), in_relative_path))
out_relative_path = "../voyages_covoit_fr/outputs/reduced_concat_covoit.csv"
out_absolute_path = os.path.abspath(os.path.join(os.getcwd(), out_relative_path))
out_absolute_folder_path = "/".join(out_absolute_path.split("/")[:-1])

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


def clean_group_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cette fonction nettoie et regroupe les données pour en garder uniquement le nécessaire.
    Les données raw étant satisfaisantes, nous nous limitons à un groupby et à la création d'une nouvelle colonne 'journey_distance_tot_passengers'.
    Cette colonne calcule la distance totale parcourue par chaque passager indépendemment d'un trip.
    Elle nous permet de connaître le nombre de km évités si tout les passagers prenaient un véhicule seul.

    :param df: Dataframe source
    :return: Dataframe groupé par jour contenant les colonnes :
        - nb_passagers : somme des passagers transportés en covoiturages via plateforme par jour
        - nb_trajets : nombre de trajets unique effectués par jour
        - total_distance : distance total parcourue, multiplié pour chaque passager.
            Ex : si un même trip transporte trois passagers, la distance est mutlitpliée par trois
    """
    df["journey_distance_tot_passengers"] = df["journey_distance"] * df["passenger_seats"]
    return (
        df.groupby("journey_start_date")
        .agg(
            nb_passagers=("passenger_seats", "sum"),
            nb_trajets=("trip_id", "nunique"),
            total_distance=("journey_distance_tot_passengers", "sum"),
        )
        .reset_index()
    )


def concat_clean_data():
    """
    Nettoie, groupe par jour certaines colonnes puis concat tout les fichiers sources historiques.
    Les résultats sont écrits dans /outputs/reduced_concat_covoit.csv
    """
    df = pd.DataFrame()
    start_time = time.time()
    for files in os.listdir(in_absolute_path):
        print(f"Processing file {in_absolute_path}/{files}...")
        df_unique = pd.read_csv(f"{in_absolute_path}/{files}", sep=";", engine="python")
        df_unique = clean_group_df(df_unique)
        df = pd.concat([df, df_unique])
    df["passenger_seats"] = df["passenger_seats"]
    print(f"Files processed in {time.time() - start_time} seconds.")
    write_data(df)


def write_data(df: pd.DataFrame):
    """
    Ecrit les données dans un fichier csv dans un dossier "outputs", créé s'il n'existe pas déjà.

    :param df: _description_
    """
    if not os.path.exists(out_absolute_folder_path):
        print(f"Creating folder '{out_absolute_folder_path}'...")
        os.makedirs(out_absolute_folder_path)
    print(f"Wrtting data to '{out_absolute_path}'...")
    df.to_csv(out_absolute_path, index=False)


concat_clean_data()
