from fmm import FastMapMatch,Network,NetworkGraph,UBODTGenAlgorithm,UBODT,FastMapMatchConfig
import os

road_data_path = "../data/porto/"
csv_file = "../data/val-gps.csv"
result_file = "../data/mr.txt"

# 加载路网数据
network = Network(os.path.join(road_data_path, "edges.shp"),"fid", "u", "v")
print("Nodes {} edges {}".format(network.get_node_count(),network.get_edge_count()))
# 构造路网拓扑
graph = NetworkGraph(network)
# 加载UBODT数据
ubodt = UBODT.read_ubodt_csv(os.path.join(road_data_path, "ubodt.txt"))
# 创建FMM模型
fmm_model = FastMapMatch(network,graph,ubodt)
# 配置匹配参数
k = 8
radius = 0.003
gps_error = 0.0005
fmm_config = FastMapMatchConfig(k,radius,gps_error)
# 配置输入GPS轨迹原始文件
'''
GPS轨迹文件格式:
id;lng;lat;feature_1;feature_2;...;feature_n
1;xxx;yyy;aaa;bbb;...;nnn
1;xxx;yyy;aaa;bbb;...;nnn
...
2;xxx;yyy;aaa;bbb;...;nnn
2;xxx;yyy;aaa;bbb;...;nnn
...
注意：
1. 每一条完整轨迹使用相同的id，同一id的数据点符合时序；
2. 除必要的三个列（id、lng、lat）外，还应该有其他之前需要的数据（例如，travel_time等）
3. 这里一定要包括日期，用来后续划分train和val-test
'''
from fmm import GPSConfig, ResultConfig
input_config = GPSConfig()
input_config.file = csv_file
input_config.id = "id"
input_config.x = "lng"
input_config.y = "lat"
input_config.gps_point = True
print(input_config.to_string())
# 配置路网匹配输出文件
result_config = ResultConfig()
result_config.file = result_file
result_config.output_config.write_opath = False
print(result_config.to_string())
# 开始路网匹配
status = fmm_model.match_gps_file(input_config, result_config, fmm_config)
print(status)
