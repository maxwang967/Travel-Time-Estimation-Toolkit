from absl import flags
from absl import logging
import pandas as pd
from pathlib import Path

FLAG = flags.FLAGS

def _extract_cpath(cpath):
    """
    Convert link path from String to List<Int>
    """
    if (isinstance(cpath, float)):
        return []
    if (cpath ==''):
        return []
    return [int(s) for s in cpath.split(',')]

def _merge() -> pd.DataFrame():
    # concat all.csv and mr.txt
    df_mr = pd.read_csv(Path(FLAG.config.work_dir) / "mr.txt", sep=";")
    df_mr["cpath_list"] = df_mr.apply(lambda row: _extract_cpath(row.cpath), axis=1)
    df_mr = df_mr.drop(columns=["mgeom", "cpath"])
    df_mr = df_mr.rename(columns={"id": "MM_ID", "cpath_list": "LINK_LIST"})
    df_all = pd.read_csv(Path(FLAG.config.output_dir) / FLAG.config.name / "all_wo_exploding.csv", sep=",")
    df_final = df_all.merge(df_mr)
    df_final = df_final[df_final["LINK_LIST"].str.len() != 0]
    del df_mr
    del df_all
    # output final csv
    return df_final

def save_final_csv() -> pd.DataFrame():
    logging.info("Generating Final Porto Dataset...")
    df_final =  _merge()
    df_final.to_csv(Path(FLAG.config.output_dir) / FLAG.config.name / "final.csv", index=False)
    logging.info("Generating Final Porto Dataset...Done")
    del df_final

