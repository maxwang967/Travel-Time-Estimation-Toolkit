from absl import flags
from absl import logging
import geopandas as gp
from pathlib import Path

FLAG = flags.FLAGS

def extract_node_edge_features():
    edge_shp = gp.GeoDataFrame.from_file(
        Path("../data/road_networks") / FLAG.config.location / "edges.shp"
    )
    node_shp = gp.GeoDataFrame.from_file(
        Path("../data/road_networks") / FLAG.config.location / "nodes.shp"
    )
    # add node_id to node shp
    node_shp["node_id"] = range(len(node_shp))
    # add node_id_1, node_id_2 to edge shp
    edge_shp["node_id_1"] = edge_shp.apply(lambda x: node_shp[node_shp.osmid == x.u].node_id.values[0], axis=1)
    edge_shp["node_id_2"] = edge_shp.apply(lambda x: node_shp[node_shp.osmid == x.v].node_id.values[0], axis=1)
    edge_shp.to_file(
        Path("../data/road_networks") / FLAG.config.location / "edges_indexed.shp"
    )
    node_shp.to_file(
        Path("../data/road_networks") / FLAG.config.location / "nodes_indexed.shp"
    )