from kf_lib_data_ingest.common.io import read_df
import glob
from graph_validator import NA, HIERARCHY, build_graph, validate_graph

DISPLAY_WIDTH = 80

def print_dir(dir):
    first_bar_width = (DISPLAY_WIDTH-2-len(dir))//2
    second_bar_width = DISPLAY_WIDTH-2-len(dir)-first_bar_width
    print("="*first_bar_width, dir, "="*second_bar_width, "\n")
    return first_bar_width+second_bar_width+len(dir)+2


for dir in [f"DATASET{i}" for i in {1, 2, 3, 4, 5}]:
    df_dict = {
        f: read_df(f, encoding="utf-8-sig").filter(HIERARCHY.nodes()).replace("NA", NA)
        for f in glob.glob(f"{dir}/*")
    }
    if df_dict:
        curl_width = print_dir(dir)
        for k, v in df_dict.items():
            print(k)
            print(v)
            print()

        graph = build_graph(df_dict)

        results = []
        for m in validate_graph(graph, df_dict):
            name = "Test: " + m.pop("Test")
            res = "Result: " + m.pop("Result")
            message = [name + " "*(curl_width-1-len(name)-len(res)) + res]
            for k, v in m.items():
                if isinstance(v, list):
                    message.append(f"{k}:")
                    for vx in sorted(v):
                        message.append("\t" + vx)
                else:
                    message.append(f"{k}: {v}")
            results.append("\n".join(message))

        print(("\n\n"+("~"*curl_width)+"\n\n").join(results))
    else:
        print(f"{dir} not found or contains no data files.")
    print()
