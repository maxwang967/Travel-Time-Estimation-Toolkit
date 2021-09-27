import sys
import os
from fmm import FastMapMatch, Network, NetworkGraph, UBODT, FastMapMatchConfig
from fmm import GPSConfig, ResultConfig
from absl import flags
from absl import logging
from pathlib import Path

FLAG = flags.FLAGS

def run_mm():
    csv_file = Path(FLAG.config.work_dir) / FLAG.config.name / "mm.csv"
    road_network_path = Path("../data/road_networks") / FLAG.config.location 
    k = FLAG.config.fmm_config.k
    radius = FLAG.config.fmm_config.radius
    gps_error = FLAG.config.fmm_config.gps_error
    work_dir = Path(FLAG.config.work_dir)
    network = Network(os.path.join(road_network_path, "edges.shp"),"fid", "u", "v")
    graph = NetworkGraph(network)
    ubodt = UBODT.read_ubodt_csv(os.path.join(road_network_path, "ubodt.txt"))
    fmm_model = FastMapMatch(network, graph, ubodt)
    fmm_config = FastMapMatchConfig(k, radius, gps_error)
    input_config = GPSConfig()
    input_config.file = csv_file
    input_config.id = "MM_ID"
    input_config.x = "LONGITUTE"
    input_config.y = "LATITIDE"
    input_config.gps_point = True
    result_config = ResultConfig()
    # result_config.file = os.path.join(work_dir, "mr.txt")
    result_config.file = Path(FLAG.config.work_dir) / "mr.txt"
    result_config.output_config.write_opath = False
    status = fmm_model.match_gps_file(input_config, result_config, fmm_config)
    print(status)
    del fmm_model
    del fmm_config
    del input_config
    del result_config