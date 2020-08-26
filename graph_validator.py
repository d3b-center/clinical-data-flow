from graph import Graph  # https://github.com/root-11/graph-theory
import itertools
from collections import defaultdict

NA = ""

HIERARCHY = Graph()
HIERARCHY.add_edge("GENOMIC_FILE|URL_LIST", "BIOSPECIMEN|ID")
HIERARCHY.add_edge("BIOSPECIMEN|ID", "PARTICIPANT|ID")
HIERARCHY.add_edge("PARTICIPANT|ID", "FAMILY|ID")


def build_graph(dict_of_dataframes):
    edges = set()
    g = Graph()

    for df in dict_of_dataframes.values():
        for row in df.to_dict(orient="records"):
            nodes = [(k, v) for k, v in row.items() if v != NA]
            # add all of the ID nodes to the main graph
            for c, n in nodes:
                g.add_node((c, n))
                g.add_edge((c, n), c)
            # put all colinear pairs into the edge graph
            for combo in itertools.combinations(nodes, 2):
                edges.add(combo)

    # Add explicit connections to the main graph from the data.

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

    edges = remaining_edges

    # (A -> B) + (B -> C) doesn't also need (A -> C)

    remaining_edges = set()

    for e in edges:
        if not g.is_connected(e[0], e[1]):
            remaining_edges.add(e)

    edges = remaining_edges

    def try_until_stable(f, edges):
        prev_num_edges = 0
        while True:
            edges = f(edges)
            if len(edges) == prev_num_edges:
                return edges
            prev_num_edges = len(edges)

    def find_attachment(base, stop_type, upwards=False):
        new_bases = set()
        def _inner(base, stop_type, new_bases):
            if upwards:
                other_nodes = [
                    n for n in g.nodes(from_node=base) 
                    if (n != base[0]) and (HIERARCHY.is_connected(n[0], stop_type))
                ]
            else:
                other_nodes = [
                    n for n in g.nodes(to_node=base) 
                    if (n != base[0]) and (HIERARCHY.is_connected(stop_type, n[0]))
                ]
            if other_nodes:
                for node in other_nodes:
                    new_bases.add(_inner(node, stop_type, new_bases))
            return base
        _inner(base, stop_type, new_bases)
        return new_bases

    # (A -> C) + (B -> C) should become (A -> B -> C)

    def acbc_abc(edges):
        remaining_edges = set()

        for a, b in edges:
            new_attachments = find_attachment(b, a[0], upwards=False)
            if new_attachments:
                for n in new_attachments:
                    g.add_edge(a, n)
            else:
                remaining_edges.add((a, b))

        return remaining_edges

    edges = try_until_stable(acbc_abc, edges)

    # (A -> C) + (A -> B) should actually be (A -> B -> C)

    def acab_abc(edges):
        remaining_edges = set()

        for a, b in edges:
            new_attachments = find_attachment(a, b[0], upwards=True)
            if new_attachments:
                for n in new_attachments:
                    g.add_edge(n, b)
            else:
                remaining_edges.add((a, b))

        return remaining_edges

    edges = try_until_stable(acab_abc, edges)

    for a, b in edges:
        g.add_edge(a, b)

    return g


def validate_graph(g, dict_of_dataframes):
    assert isinstance(g, Graph)
    assert len(g.nodes()) > 0

    def test_connections(first_type, second_type, validator):
        upwards = second_type in HIERARCHY.nodes(from_node=first_type)
        errors = []
        for n in g.nodes(to_node=first_type):
            if upwards:
                links = [c for c in g.nodes(from_node=n) if c[0] == second_type]
            else:
                links = [c for c in g.nodes(to_node=n) if c[0] == second_type]
            if not validator(len(links)):
                errors.append({"from": n, "to": links})
        return errors

    def find_in_files(nodes):
        found = defaultdict(list)
        for n in nodes:
            for f, df in dict_of_dataframes.items():
                if (n[0] in df) and (n[1] in df[n[0]].values):
                    found[n].append(f)
        return [f"{k} found in {v}" for k, v in found.items()]

    def message_dict(description, errors):
        details = []
        nodes = set()
        for e in errors:
            details.append(f"{e['from']} -> {e['to']}")
            nodes.add(e["from"])
            nodes.update(e["to"])
        message = {
            "Test": description,
            "Result": "❌" if errors else "✅"
        }
        if errors:
            message["Error Reasons"] = details
            message["Locations"] = find_in_files(nodes)
        return message

    messages = [
        message_dict(
            "Each Biospecimen comes from 1 Participant",
            test_connections("BIOSPECIMEN|ID", "PARTICIPANT|ID", lambda x: x == 1)
        ),
        message_dict(
            "Each Participant has at least 1 Biospecimen",
            test_connections("PARTICIPANT|ID", "BIOSPECIMEN|ID", lambda x: x >= 1)
        ),
        message_dict(
            "Each Participant has at least 1 Family",
            test_connections("PARTICIPANT|ID", "FAMILY|ID", lambda x: x >= 1)
        ),
        message_dict(
            "Each Family has at least 1 Participant",
            test_connections("FAMILY|ID", "PARTICIPANT|ID", lambda x: x >= 1)
        ),
        message_dict(
            "Each Source Genomic File comes from 1 Biospecimen",
            test_connections("GENOMIC_FILE|URL_LIST", "BIOSPECIMEN|ID", lambda x: x == 1)
        )
    ]
    return messages
