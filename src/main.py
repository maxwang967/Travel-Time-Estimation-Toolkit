from absl import app
from absl import flags
from absl import logging
from ml_collections import config_flags
from preprocessing import generate_csv_for_map_matching
from postprocessing import save_final_pickle
import os
from pathlib import Path
import subprocess
from road_networks import extract_node_edge_features

from visualize import visualize_trajectory

FLAG = flags.FLAGS
config_flags.DEFINE_config_file(
    'config', None, 'File path for map matching configuration')


def main(argv):
    if len(argv) > 1:
        raise app.UsageError('Too many command-line arguments.')
    # io check, create work and output directories
    (Path(FLAG.config.work_dir) / FLAG.config.name).mkdir(parents=True, exist_ok=True)
    (Path(FLAG.config.output_dir) / FLAG.config.name).mkdir(parents=True, exist_ok=True)
    # Mode: Data Preprocessing
    if FLAG.config.mode == "data_preprocessing":
        logging.info("Mode: Data preprocessing")
        # preprocess the raw dataset
        if not FLAG.config.is_mm_after_only:
            if FLAG.config.is_raw_data:
                generate_csv_for_map_matching(FLAG.config)
            # skip the map matching
            if FLAG.config.is_preprocessing_only:
                logging.info("Everything is done.")
                return
        # map matching: get the mr.txt
        # csv_file = os.path.join(FLAG.config.work_dir, "mm.csv")
        logging.info("Running Map Matching...")
        # mm_command = f"/usr/bin/python2 map_matching.py {csv_file} {os.path.join('../data/road_networks', FLAG.config.location)} {FLAG.config.fmm_config.k} {FLAG.config.fmm_config.radius} {FLAG.config.fmm_config.gps_error} {FLAG.config.work_dir}"
        # mm_process = subprocess.Popen(mm_command.split(), stdout=subprocess.PIPE)
        # output, _ = mm_process.communicate()
        # logging.info(f"Map Matching Output: {output}")
        logging.info("Map Matching Done.")
        # post preprocessing
        save_final_pickle()
    # Mode: Visualize Trajectories
    elif FLAG.config.mode == "visualize_trajectory":
        logging.info("Mode: Trajectory Visualization")
        visualize_trajectory()
    elif FLAG.config.mode == "extract_road_network_information":
        logging.info("Mode: Road Network Information Extraction")
        logging.info("Extracting road network features...")
        extract_node_edge_features()
        logging.info("Extracting road network features...Done")



if __name__ == '__main__':
    flags.mark_flags_as_required(['config'])
    app.run(main)
