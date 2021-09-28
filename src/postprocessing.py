from absl import flags
from absl import logging
import pandas as pd
from pathlib import Path
from utils import extract_cpath

FLAG = flags.FLAGS




def _merge() -> pd.DataFrame():
    # concat all.csv and mr.txt
    df_mr = pd.read_csv(Path(FLAG.config.work_dir) / FLAG.config.name / "mr.txt", sep=";")
    df_mr["cpath_list"] = df_mr.apply(lambda row: extract_cpath(row.cpath), axis=1)
    df_mr = df_mr.drop(columns=["mgeom", "cpath"])
    df_mr = df_mr.rename(columns={"id": "MM_ID", "cpath_list": "LINK_LIST"})
    df_all = pd.read_csv(Path(FLAG.config.output_dir) / FLAG.config.name / "all_wo_exploding.csv", sep=",")
    df_final = df_all.merge(df_mr)
    df_final = df_final[df_final["LINK_LIST"].str.len() != 0]
    del df_mr
    del df_all
    # output final csv
    return df_final


def _clean_final_pickle(df_final):
    # TODO can add other removing rules
    # remove travel time <= 0
    df_final = df_final[df_final.TRAVEL_TIME > 0]
    return df_final


def save_final_pickle() -> pd.DataFrame():
    logging.info("Generating Final Dataset...")
    df_final =  _merge()
    df_final = _clean_final_pickle(df_final)
    df_final.to_pickle(Path(FLAG.config.output_dir) / FLAG.config.name / "final.pkl")
    logging.info("Generating Final Dataset...Done")
    del df_final