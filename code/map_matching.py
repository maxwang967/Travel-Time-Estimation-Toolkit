# This file is for python 2.7 which supports FMM
import sys
import os
from fmm import FastMapMatch, Network, NetworkGraph, UBODT, FastMapMatchConfig
from fmm import GPSConfig, ResultConfig

def main():
    csv_file = sys.argv[1]
    road_network_path = sys.argv[2]
    k = int(sys.argv[3])
    radius = float(sys.argv[4])
    gps_error = float(sys.argv[5])
    work_dir = sys.argv[6]
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
    result_config.file = os.path.join(work_dir, "mr.txt")
    result_config.output_config.write_opath = False
    status = fmm_model.match_gps_file(input_config, result_config, fmm_config)
    print(status)
    del fmm_model
    del fmm_config
    del input_config
    del result_config


if __name__ == '__main__':
    main()