import glob
import os

import pygraphviz as pgv
from kf_lib_data_ingest.common.io import read_df

from graph_validator import (
    HIERARCHY,
    NA,
    build_graph,
    report_type_counts,
    validate_graph
)


def draw_graph(name, graph):
    G = pgv.AGraph(directed=True)
    for e in graph.edges():
        if e[0][0] != e[1]:
            G.add_edge(e[0], e[1])
    fname = f"{name}.png"
    try:
        os.remove(fname)
    except OSError:
        pass
    G.draw(fname, format="png", prog="dot")
    print(fname)
    print(f"\n![\"Generated Graph Image\"]({fname})\n")



for dir in sorted(glob.glob("DATASET*")):
    df_dict = {}
    for f in glob.glob(f"{dir}/*"):
        try:
            df_dict[f] = read_df(f, encoding="utf-8-sig")
            df_dict[f] = df_dict[f].filter(HIERARCHY.nodes()).replace("NA", NA)
        except:
            continue

    if df_dict:
        print(f"## {dir}\n")
        print("```text")
        first_bar_width = (88 - len(dir)) // 2
        second_bar_width = 88 - len(dir) - first_bar_width
        divider_width = first_bar_width + second_bar_width + len(dir) + 2
        print("=" * divider_width)
        print("=" * first_bar_width, dir, "=" * second_bar_width)
        print("=" * divider_width, "\n")

        input_graph = build_graph(df_dict, implicit=False)
        graph = build_graph(df_dict)

        print("NODE TYPE COUNTS:")
        counts = report_type_counts(graph)
        colwidth = len(max(counts, key=len))
        for k, v in counts.items():
            print(f"\t{k:<{colwidth}} : {v}")

        print()

        results = []
        for m in validate_graph(graph, df_dict):
            name = "Test: " + m.pop("Test")
            result = "Result: " + m.pop("Result")
            gap = " " * (divider_width - 1 - len(name) - len(result))
            message = [f"{name}{gap}{result}"]
            for k, v in m.items():
                message.append(f"\n{k}:")
                for vx in sorted(v):
                    message.append("\t" + vx)
            results.append("\n".join(message))

        print(f"\n\n{'~' * divider_width}\n\n".join(results))

        print("```")
        print("\n### Input and output images...\n")
        draw_graph(f"{dir}/input", input_graph)
        draw_graph(f"{dir}/output", graph)
    else:
        print(f"{dir} not found or contains no data files.")
    print()
