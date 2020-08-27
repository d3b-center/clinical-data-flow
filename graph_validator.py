import itertools
from collections import defaultdict

from graph import Graph  # https://github.com/root-11/graph-theory

from relations import HIERARCHY, REVERSE_TESTS, TESTS

NA = ""


def build_graph(dict_of_dataframes):
    g = Graph()
    edges = set()

    ######## Add IDs to the graph and record colinear pairs as edges ########

    for df in dict_of_dataframes.values():
        for row in df.to_dict(orient="records"):
            nodes = [(k, v) for k, v in row.items() if v != NA]
            for c, n in nodes:
                g.add_node((c, n))
                g.add_edge((c, n), c)  # relate each ID to its type
            for combo in itertools.combinations(nodes, 2):
                edges.add(combo)

    ######## Add explicit (direct hierarchy) connections to the graph ########

    remaining_edges = set()
    for a, b in edges:
        if b[0] in HIERARCHY.nodes(from_node=a[0]):
            g.add_edge(a, b)
        elif a[0] in HIERARCHY.nodes(from_node=b[0]):
            g.add_edge(b, a)
        else:
            if HIERARCHY.is_connected(a[0], b[0]):
                remaining_edges.add((a, b))
            else:
                remaining_edges.add((b, a))

    ########################################################################
    ######## Code beyond here is for indirectly implied connections ########
    ########################################################################

    def prune_unneeded(edges):
        # Prune remaining edges: (A -> B) + (B -> C) doesn't also need (A -> C)
        g.is_connected.cache_clear()
        return [e for e in edges if not g.is_connected(e[0], e[1])]

    edges = prune_unneeded(remaining_edges)

    ######## (A -> C) + (B -> C) should become (A -> B -> C) ########

    def acbc_abc(edges):
        new_edges = set()
        for e in edges:
            a, b = e
            new_dests = [
                n
                for n in g.nodes(to_node=b)
                if HIERARCHY.is_connected(a[0], n[0])
            ]
            if new_dests:
                for n in new_dests:
                    if HIERARCHY.edge(a[0], n[0]):
                        g.add_edge(a, n)
                    else:
                        new_edges.add((a, n))
            else:
                new_edges.add(e)
        return new_edges

    ######## (A -> C) + (A -> B) should actually be (A -> B -> C) ########

    def acab_abc(edges):
        new_edges = set()
        for e in edges:
            a, b = e
            new_dests = [
                n
                for n in g.nodes(from_node=a)
                if (n != a[0]) and HIERARCHY.is_connected(n[0], b[0])
            ]
            if new_dests:
                for n in new_dests:
                    if HIERARCHY.edge(n[0], b[0]):
                        g.add_edge(n, b)
                    else:
                        new_edges.add((n, b))
            else:
                new_edges.add(e)
        return new_edges

    ###### Shake the graph back and forth ######

    def try_until_stable(f, edges):
        prev_edges = edges
        while True:
            edges = f(edges)
            if edges == prev_edges:
                return edges
            prev_edges = edges

    def shake(edges):
        edges = acbc_abc(edges)
        edges = acab_abc(edges)
        return edges

    edges = try_until_stable(shake, edges)

    ######## Add remaining unmovable edges to the graph ########

    for a, b in prune_unneeded(edges):
        g.add_edge(a, b)

    return g


def report_type_counts(g):
    return {c: len(g.nodes(to_node=c)) for c in reversed(HIERARCHY.nodes())}


def validate_graph(g, dict_of_dataframes):
    assert isinstance(g, Graph)
    assert len(g.nodes()) > 0

    def find_in_files(nodes):
        found = defaultdict(list)
        for n in nodes:
            for f, df in dict_of_dataframes.items():
                if (n[0] in df) and (n[1] in df[n[0]].values):
                    found[n].append(f)
        return [f"{k} found in {v}" for k, v in found.items()]

    def test(typeA, typeB, relation):
        eval_text, eval_func = relation
        errors = []
        nodes_to_check = g.nodes(to_node=typeA)
        for n in nodes_to_check:
            from_n = n if typeB in HIERARCHY.nodes(from_node=typeA) else None
            to_n = n if not from_n else None
            links = [c for c in g.nodes(from_n, to_n) if c[0] == typeB]
            if not eval_func(len(links)):
                errors.append({"from": n, "to": links})

        emoji = "⛔" if not nodes_to_check else "❌" if errors else "✅"
        description = f"Each {typeA} links to {eval_text} 1 {typeB}"
        message = {"Test": description, "Result": emoji}
        details = []
        nodes = set()
        for e in errors:
            details.append(f"{e['from']} -> {e['to']}")
            nodes.add(e["from"])
            nodes.update(e["to"])
        if errors:
            message["Error Reasons"] = details
            message["Locations"] = find_in_files(nodes)
        return message

    m1 = [test(a, b, TESTS[r]) for a, b, r in HIERARCHY.edges()]
    m2 = [test(b, a, REVERSE_TESTS[r]) for a, b, r in HIERARCHY.edges()]
    return reversed(list(itertools.chain.from_iterable(zip(m1, m2))))
