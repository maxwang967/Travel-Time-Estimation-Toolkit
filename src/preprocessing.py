import ml_collections
import pandas as pd
from pathlib import Path

def generate_csv_for_map_matching(config: ml_collections.ConfigDict()):
    df_csv: pd.DataFrame = config.converter(config.data_dir)
    # "all.csv" is the csv file for overall information
    df_csv.to_csv(Path(config.output_dir) / config.name / "all.csv", index=False)
    df_csv = df_csv.drop(columns=["TRIP_ID", "TAXI_ID", "TIMESTAMP", "TRAVEL_TIME"])
    # "mm.csv" is the csv file for map matching 
    df_csv.to_csv(Path(config.work_dir) / config.name / "mm.csv", index=False, sep=";")
    del df_csv