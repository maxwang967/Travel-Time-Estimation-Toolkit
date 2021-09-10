import pandas as pd
from absl import logging
from absl import flags
from pathlib import Path

FLAG = flags.FLAGS

def get_porto_dataset_mm_csv(root_path):
    """
    Get mm csv for Porto dataset
    Url: https://www.kaggle.com/crailtap/taxi-trajectory
    The files must be saved in this function are:
    1. all_wo_exploding.csv
    """
    csv_path = Path(root_path) / "train.csv"
    logging.info("Converting Porto Dataset...")
    if FLAG.config.debug:
        df_raw = pd.read_csv(csv_path, sep=",", nrows=1000)
    else:
        df_raw = pd.read_csv(csv_path, sep=",")
    # remove missing data rows
    df_raw = df_raw[df_raw["MISSING_DATA"] == False]
    df_raw = df_raw.drop(columns=["MISSING_DATA"])
    # transform trajectories to list
    df_raw["TRAJ"] = df_raw.apply(lambda x: eval(x.POLYLINE), axis=1)
    df_raw = df_raw.drop(columns=["POLYLINE", "ORIGIN_CALL", "ORIGIN_STAND", "DAY_TYPE", "CALL_TYPE"])
    df_raw = df_raw[df_raw["TRAJ"].map(len) > 0]
    # unique id for map matching
    df_raw["MM_ID"] = range(1, len(df_raw) + 1, 1)
    # travel time in seconds
    df_raw["TRAVEL_TIME"] = df_raw.apply(lambda x: (len(x.TRAJ) - 1) * 15, axis=1)
    # save important factors before exploding
    df_raw.drop(columns=["TRAJ"]).to_csv(Path(FLAG.config.output_dir) / FLAG.config.name / "all_wo_exploding.csv", index=False)
    # explode by traj (i.e. expand the list in TRAJ to multiple rows)
    df_raw = df_raw.explode("TRAJ")
    df_raw["LONGITUTE"] = df_raw.apply(lambda x: x.TRAJ[0], axis=1)
    df_raw["LATITIDE"] = df_raw.apply(lambda x: x.TRAJ[1], axis=1)
    df_raw = df_raw.drop(columns=["TRAJ"])
    logging.info("Converting Porto Dataset...Done")
    return df_raw