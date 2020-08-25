from kf_lib_data_ingest.common.io import read_df
import glob
from graph_validator import NA, HIERARCHY, build_graph, validate_graph

for dir in ["DATASET1", "DATASET2"]:
    df_list = [
        read_df(f, encoding="utf-8-sig").filter(HIERARCHY.nodes()).replace("NA", NA)
        for f in glob.glob(f"{dir}/*")
    ]
    if df_list:
        print(dir)
        graph, remaining_edges = build_graph(df_list)
        validate_graph(graph)
    else:
        print(f"{dir} not found or contains no data files.")
