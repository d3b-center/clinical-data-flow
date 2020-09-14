import itertools
from collections import defaultdict

from graph import Graph  # https://github.com/root-11/graph-theory

from relations import HIERARCHY, REVERSE_TESTS, TESTS

NA = ""


def build_graph(dict_of_dataframes, include_implicit=True):
    graph = Graph()
    edges = set()

    ######## Add nodes and record colinear pairs as potential edges ########

    for df in dict_of_dataframes.values():
        for row in df.to_dict(orient="records"):
            nodes = [(k, v) for k, v in row.items() if v != NA]
            for c, n in nodes:
                graph.add_node((c, n))
                graph.add_edge((c, n), c)  # relate each node to its type
            for combo in itertools.combinations(nodes, 2):
                edges.add(combo)

    ######## Add explicit (direct hierarchy) connections to the graph ########

    remaining_edges = set()
    ignored_edges = set()

    for a, b in edges:
        if b[0] in HIERARCHY.nodes(a[0]):
            graph.add_edge(a, b)
        elif a[0] in HIERARCHY.nodes(b[0]):
            graph.add_edge(b, a)
        else:
            if HIERARCHY.is_connected(a[0], b[0]):
                remaining_edges.add((a, b))
            elif HIERARCHY.is_connected(b[0], a[0]):
                remaining_edges.add((b, a))
            else:
                ignored_edges.add((a, b))

    def prune_unneeded(edges):
        # (A -> B) + (B -> C) doesn't also need (A -> C)
        graph.is_connected.cache_clear()
        return [e for e in edges if not graph.is_connected(e[0], e[1])]

    edges = prune_unneeded(remaining_edges)

    if include_implicit:
        ######################################################################
        ########  Code in here is for indirectly implied connections  ########
        ######################################################################

        ######## (A -> C) + (B -> C) should become (A -> B -> C) ########

        def acbc_abc(edges):
            new_edges = set()
            for e in edges:
                a, b = e
                new_dests = [
                    n
                    for n in graph.nodes(to_node=b)
                    if HIERARCHY.is_connected(a[0], n[0])
                ]
                if new_dests:
                    for n in new_dests:
                        if HIERARCHY.edge(a[0], n[0]):
                            graph.add_edge(a, n)
                        else:
                            # We can track movements here for detailed error output
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
                    for n in graph.nodes(a)
                    if (n != a[0]) and HIERARCHY.is_connected(n[0], b[0])
                ]
                if new_dests:
                    for n in new_dests:
                        if HIERARCHY.edge(n[0], b[0]):
                            graph.add_edge(n, b)
                        else:
                            # We can track movements here for detailed error output
                            new_edges.add((n, b))
                else:
                    new_edges.add(e)
            return new_edges

        ###### Shake the graph back and forth until placements stabilize ######

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

        edges = prune_unneeded(try_until_stable(shake, edges))

    ######## Throw remaining edges into the graph ########

    # TBD: REPLACE THIS WITH LEAST COMMON ANCESTOR DISCOVERY?
    for e in edges:
        graph.add_edge(a, b)

    return graph, ignored_edges


def get_type_counts(graph):
    return {c: len(graph.nodes(to_node=c)) for c in reversed(HIERARCHY.nodes())}


def validate_graph(graph, dict_of_dataframes):
    assert isinstance(graph, Graph)
    assert len(graph.nodes()) > 0

    membership_lookup = {
        f: {col: set(df[col].values) for col in df.columns}
        for f, df in dict_of_dataframes.items()
    }
    dict_of_dataframes = None

    def find_in_files(node):
        found = []
        for f, ml in membership_lookup.items():
            if (node[0] in ml) and (node[1] in ml[node[0]]):
                found.append(f)
        return found

    def format_result(desc, valid, errors):
        return {"description": desc, "is_applicable": valid, "errors": errors}

    def cardinality(typeA, typeB, relation):
        # Tests cardinality of connections between typeA and typeB
        eval_text, eval_func = relation
        errors = []
        A_nodes = graph.nodes(to_node=typeA)
        for n in A_nodes:
            from_n = n if typeB in HIERARCHY.nodes(typeA) else None
            to_n = None if from_n else n
            links = [c for c in graph.nodes(from_n, to_n) if c[0] == typeB]
            if not eval_func(len(links)):
                locs = {m: find_in_files(m) for m in ([n] + links)}
                errors.append({"from": n, "to": links, "locations": locs})

        description = f"Each {typeA} links to {eval_text} {typeB}"
        return format_result(description, bool(A_nodes), errors)

    def gaps():
        # Tests that A always -> B always -> C and not A -> C without a B
        errors = []
        for n in graph.nodes():
            links = [
                m
                for m in graph.nodes(from_node=n)
                if (n[0] != m) and (m[0] not in HIERARCHY.nodes(from_node=n[0]))
            ]
            if links:
                locs = {m: find_in_files(m) for m in ([n] + links)}
                errors.append({"from": n, "to": links, "locations": locs})

        description = "All resolved links are direct without gaps in hierarchy"
        return format_result(description, bool(graph.nodes()), errors)

    for a, b, r in HIERARCHY.edges():
        if r in TESTS:
            yield cardinality(a, b, TESTS[r])
        if r in REVERSE_TESTS:
            yield cardinality(b, a, REVERSE_TESTS[r])

    yield gaps()
