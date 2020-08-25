from pprint import pprint
from graph import Graph  # https://github.com/root-11/graph-theory
import itertools


NA = ""

HIERARCHY = Graph()
HIERARCHY.add_edge("GENOMIC_FILE|URL_LIST", "BIOSPECIMEN|ID")
HIERARCHY.add_edge("BIOSPECIMEN|ID", "PARTICIPANT|ID")
HIERARCHY.add_edge("PARTICIPANT|ID", "FAMILY|ID")


def build_graph(iterable_of_dataframes):
    edges = Graph()
    g = Graph()

    for df in iterable_of_dataframes:
        for row in df.to_dict(orient="records"):
            nodes = [(k, v) for k, v in row.items() if v != NA]
            # add all of the ID nodes to the main graph
            for c, n in nodes:
                g.add_node((c, n))
                g.add_edge((c, n), c)
            # put all colinear pairs into the edge graph
            for combo in itertools.combinations(nodes, 2):
                edges.add_edge(combo[0], combo[1])

    # Add explicit connections to the main graph from the data.

    remaining_edges = Graph()

    for a, b, _ in edges.edges():
        if b[0] in HIERARCHY.nodes(from_node=a[0]):
            g.add_edge(a, b)
        elif a[0] in HIERARCHY.nodes(from_node=b[0]):
            g.add_edge(b, a)
        else:
            remaining_edges.add_edge(a, b)

    edges = remaining_edges

    # Prune unneeded indirect connections from the remaining data.
    # (A -> B -> C) already captures (A -> C)

    remaining_edges = Graph()

    for a, b, _ in edges.edges():
        if not (g.is_connected(a, b) or g.is_connected(a, b)):
            remaining_edges.add_edge(a, b)

    edges = remaining_edges

    # Find connection points in the main graph for implied links.
    # Given (A -> C) and (B -> C), infer (A -> B -> C) if C has one B.

    def connect_first_to_descendant_of_second(a, b):
        n = b
        while n[0] != a[0]:
            children = g.nodes(to_node=n)
            if len(children) > 1:
                print(f"Ambiguous relationship discovered between {a} and {b}.")
                print(f" - {n} has multiple children.")
                return False
            elif len(children) == 0:
                if n != b:
                    g.add_edge(a, n)
                    return False
                else:
                    # B is an orphan. We'll try to percolate it up A's other links when this phase is done.
                    return True
            elif len(children) == 1:
                n = children[0]

    prev_num_edges = 0
    while True:
        remaining_edges = Graph()

        for a, b, _ in edges.edges():
            if HIERARCHY.is_connected(a[0], b[0]):
                res = connect_first_to_descendant_of_second(a, b)
                if res:
                    remaining_edges.add_edge(a, b)
            elif HIERARCHY.is_connected(b[0], a[0]):
                res = connect_first_to_descendant_of_second(b, a)
                if res:
                    remaining_edges.add_edge(b, a)
            else:
                remaining_edges.add_edge(a, b)

        edges = remaining_edges
        if len(edges.edges()) == prev_num_edges:
            break
        prev_num_edges = len(edges.edges())

    # Percolate remaining graph relationships that were lower than they should be

    node_types = set(HIERARCHY.nodes())

    def find_roots(base_node, roots):
        parents = [g for g in g.nodes(from_node=base_node) if g != base_node[0]]
        if parents:
            for node in parents:
                find_roots(node, roots)
        else:
            roots.add(base_node)

    remaining_edges = Graph()

    for e in edges.edges():
        roots = set()
        find_roots(e[0], roots)
        if roots:
            for r in roots:
                g.add_edge(r, e[1])
        else:
            remaining_edges.add_edge(e[0], e[1])

    return g, remaining_edges


def validate_graph(g):
    assert isinstance(g, Graph)
    assert len(g.nodes()) > 0
    def test_connections(first_type, second_type, validator):
        upwards = second_type in HIERARCHY.nodes(from_node=first_type)
        test_errors = []
        for n in g.nodes(to_node=first_type):
            if upwards:
                links = [c for c in g.nodes(from_node=n) if c[0] == second_type]
            else:
                links = [c for c in g.nodes(to_node=n) if c[0] == second_type]
            if not validator(len(links)):
                test_errors.append(f"{n} -> {links}")

        if test_errors:
            print("\tTest Failed:")
            for e in test_errors:
                print(f"\t\t{e}")
        else:
            print("\tTest Passed")

    # TEST: each specimen links to exactly one participant
    test_connections("BIOSPECIMEN|ID", "PARTICIPANT|ID", lambda x: x == 1)

    # TEST: each participant links to at least one specimen
    test_connections("PARTICIPANT|ID", "BIOSPECIMEN|ID", lambda x: x >= 1)

    # TEST: each participant links to at least one family group
    test_connections("PARTICIPANT|ID", "FAMILY|ID", lambda x: x >= 1)

    # TEST: each family group links to at least one participant
    test_connections("FAMILY|ID", "PARTICIPANT|ID", lambda x: x >= 1)

    # TEST: each source file links to exactly one biospecimen
    test_connections("GENOMIC_FILE|URL_LIST", "BIOSPECIMEN|ID", lambda x: x == 1)
