from absl import flags, logging
import pandas as pd
from pathlib import Path
from utils import extract_cpath
import numpy as np
import geopandas as gpd

FLAG = flags.FLAGS

def visualize_trajectory():
    config = FLAG.config
    # pre-load matched routes
    df_mr = pd.read_csv(Path(config.work_dir) / config.name / "mr.txt", sep=";")
    df_mr["cpath_list"] = df_mr.apply(lambda row: extract_cpath(row.cpath), axis=1)
    # pre-load matched-edges file to obtain mapping (fid -> geometry)
    if (Path(config.work_dir) / config.name / "matched_edges.csv").is_file():
        df_me = pd.read_csv(
            Path(config.work_dir) / config.name / "matched_edges.csv",
            sep=";"
        )
    else:
        logging.info("Generating Matched Edges...")
        all_edge_ids = np.unique(np.hstack(df_mr.cpath_list)).tolist()
        network_gdf = gpd.read_file(Path("../data/road_networks") / config.location / "edges.shp")
        network_gdf.id = network_gdf.fid.astype(int)
        df_me = network_gdf[network_gdf.id.isin(all_edge_ids)].reset_index()
        df_me["points"] = df_me.apply(lambda row: len(row.geometry.coords), axis=1)
        df_me[["fid","u","v","geometry","points"]].to_csv(Path(config.work_dir) / "matched_edges.csv",sep=";",index=False)
        del 
        logging.info("Generating Matched Edges...Done")
