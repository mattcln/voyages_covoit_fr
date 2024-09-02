import os
import time

import pandas as pd

in_relative_path = "../voyages_covoit_fr/exports_covoit/"
in_absolute_path = os.path.abspath(os.path.join(os.getcwd(), in_relative_path))
out_relative_path = "../voyages_covoit_fr/outputs/reduced_concat_covoit_full.csv"
out_absolute_path = os.path.abspath(os.path.join(os.getcwd(), out_relative_path))
out_absolute_folder_path = "/".join(out_absolute_path.split("/")[:-1])


def data_quality_checks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cette fonction check plusieurs point de qualité des données :
    - Distance et temps supérieur à 0
    - Nombre de passagers entre 1 et 6 (compris)

    Si une ligne ne respecte pas ces points, elle est ignorée et un warning est loggé.

    :param df: Dataframe source
    :return: Dataframe sans lignes incohérentes
    """
    nb_dist_dur_zero = len(df[(df["journey_distance"] <= 0) & (df["journey_duration"] <= 0)])
    if nb_dist_dur_zero:
        print(f"Removing {nb_dist_dur_zero} rows with a distance or a duration <= 0.")
        df = df[~(df["journey_distance"] <= 0) | ~(df["journey_duration"] <= 0)].copy()

    nb_passenger_seats_incoherent = len(df[(df["passenger_seats"] <= 0) | (df["passenger_seats"] > 6)])
    if nb_passenger_seats_incoherent:
        print(f"Removing {nb_passenger_seats_incoherent} rows with a number of passenger seats not between 1 and 6.")
        df = df[~(df["passenger_seats"] <= 0) & ~(df["passenger_seats"] > 6)].copy()

    return df


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
    df = data_quality_checks(df)
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
    print(f"Files processed in {time.time() - start_time} seconds.")
    write_data(df.sort_values("journey_start_date"))


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


if __name__ == "__main__":
    concat_clean_data()
