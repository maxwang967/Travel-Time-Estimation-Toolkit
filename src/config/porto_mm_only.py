import ml_collections
from converts import get_porto_dataset_mm_csv

def get_config():
    config = ml_collections.ConfigDict()
    # name of configuration file
    config.name = "porto"
    # selected mode (i.e. data_preprocessing, visualize_trajectory)
    config.mode = "data_preprocessing"
    # determine if debug mode
    config.debug = False
    # determine if launch data adaption 
    config.is_raw_data = True
    # determine if preprocessing only
    config.is_preprocessing_only = True
    # determine if mm and postprocessing only
    config.is_mm_after_only = True
    # data converter for raw data
    config.converter = get_porto_dataset_mm_csv
    # directory for porto raw dataset (i.e. relative path from the directory "main.py" located in)
    config.data_dir = "../data/raw_data/porto"
    # temporary directory for immediate files (i.e. relative path from the directory "main.py" located in)
    config.work_dir = "../work_dir"
    # output directory (i.e. relative path from the directory "main.py" located in)
    config.output_dir = "../data/preprocessed_data"
    # location of the road network (i.e. chengdu, porto)
    config.location = "porto"
    # configuration for FMM (cf. https://fmm-wiki.github.io/docs/documentation/configuration/)
    config.fmm_config = ml_collections.ConfigDict()
    config.fmm_config.k = 8
    config.fmm_config.radius = 0.003
    config.fmm_config.gps_error = 0.0005
    return config


