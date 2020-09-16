import glob
import os

import pygraphviz as pgv
from kf_lib_data_ingest.common.io import read_df

from graph_validator import NA, build_graph, get_type_counts, validate_graph
from relations import HIERARCHY


def draw_graph(name, graph):
    G = pgv.AGraph(directed=True)
    for e in graph.edges():
        if e[0][0] != e[1]:
            G.add_edge(e[0], e[1])

    fname = f"{name}.svg"
    try:
        os.remove(fname)
    except OSError:
        pass
    G.draw(fname, format="svg", prog="dot")
    print(fname)
    print(f'\n!["Generated Graph Image"]({fname})\n')


def message_from_result(result, width):
    description = result["description"]
    valid = result["is_applicable"]
    errors = result["errors"]
    name = "Test: " + description
    status = "⛔" if not valid else "❌" if errors else "✅"
    message = [f"{status} {name}"]
    if errors:
        parts = {}
        if result["type"] == "relationship":
            parts["Error Reasons"] = [
                f"{e['from']} -> {sorted(e['to'])}" for e in errors
            ]
            parts["Locations"] = [
                f"{k} is in {v}" for e in errors for k, v in e["locations"].items()
            ]
            for k, v in parts.items():
                message.append(f"\n{k}:")
                for vx in sorted(v):
                    message.append(f"\t{vx}")
        elif result["type"] == "attribute":
            for k, v in errors.items():
                message.append(f"\n{k} contains bad values:")
                for vx in sorted(v):
                    message.append(f"\t\"{vx}\"")

    return "\n".join(message)


# DIRS = sorted(glob.glob("DATASET*"))
DIRS = [
    "/Users/kelmana/Documents/kids-first/kf-ingest-packages/kf_ingest_packages/packages/SD_BHJXBDQK/output/ExtractStage"
]

for dir in DIRS:
    df_dict = {}
    for f in glob.glob(f"{dir}/*"):
        try:
            fname = os.path.basename(f)
            df_dict[fname] = read_df(f, encoding="utf-8-sig")
            df_dict[fname] = (
                df_dict[fname].filter(HIERARCHY.nodes()).replace("NA", NA)
            )
        except:
            continue

    if df_dict:
        print(f"## {dir}\n\n```text")
        spaced_dir = f" {dir} "
        divider = 90 * "="
        first_bar_width = (len(divider) - len(spaced_dir)) // 2
        second_bar_width = len(divider) - len(spaced_dir) - first_bar_width
        print(divider)
        print(f"{'=' * first_bar_width} {spaced_dir} {'=' * second_bar_width}")
        print(f"{divider}\n")
        print("Loaded files:")
        for f in df_dict:
            print(os.path.join(dir, f))
        print()

        input_graph = build_graph(df_dict, include_implicit=False)
        graph = build_graph(df_dict)

        count_block = ["NODE TYPE COUNTS:"]
        counts = get_type_counts(graph)
        colwidth = len(max(counts.keys(), key=len))
        count_block += [f"\t{k:<{colwidth}} : {v}" for k, v in counts.items()]

        print("\n".join(count_block))

        for r in validate_graph(graph, df_dict):
            print(f"\n{'~' * len(divider)}\n")
            print(message_from_result(r, len(divider)))

        print("```")
        # print("\n### Input and output images...\n")
        # draw_graph(f"{dir}/input", input_graph)
        # draw_graph(f"{dir}/output", graph)
    else:
        print(f"{dir} not found or contains no data files.")

    print()
