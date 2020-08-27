import glob

from kf_lib_data_ingest.common.io import read_df

from graph_validator import (
    HIERARCHY,
    NA,
    build_graph,
    report_type_counts,
    validate_graph,
)

for dir in sorted(glob.glob("DATASET*")):
    df_dict = {
        f: read_df(f, encoding="utf-8-sig")
        .filter(HIERARCHY.nodes())
        .replace("NA", NA)
        for f in glob.glob(f"{dir}/*")
    }
    if df_dict:
        first_bar_width = (88 - len(dir)) // 2
        second_bar_width = 88 - len(dir) - first_bar_width
        divider_width = first_bar_width + second_bar_width + len(dir) + 2
        print("=" * divider_width)
        print("=" * first_bar_width, dir, "=" * second_bar_width)
        print("=" * divider_width, "\n")
        for k, v in df_dict.items():
            print(k)
            print(v)
            print()
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
    else:
        print(f"{dir} not found or contains no data files.")
    print()
