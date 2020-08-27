from graph import Graph  # https://github.com/root-11/graph-theory

MANY_ONE = 1
MANY_MANY = 2
ONE_MANY = 3
ONE_ONE = 4

RELATIONS = {
    "ONE": ("exactly", lambda x: x == 1),
    "MANY": ("at least", lambda x: x >= 1),
}

TESTS = {
    MANY_ONE: RELATIONS["ONE"],
    MANY_MANY: RELATIONS["MANY"],
    ONE_MANY: RELATIONS["MANY"],
    ONE_ONE: RELATIONS["ONE"],
}

REVERSE_TESTS = {
    MANY_ONE: RELATIONS["MANY"],
    MANY_MANY: RELATIONS["MANY"],
    ONE_MANY: RELATIONS["ONE"],
    ONE_ONE: RELATIONS["ONE"],
}

HIERARCHY = Graph()
HIERARCHY.add_edge("GENOMIC_FILE|URL_LIST", "BIOSPECIMEN|ID", MANY_ONE)
HIERARCHY.add_edge("BIOSPECIMEN|ID", "PARTICIPANT|ID", MANY_ONE)
HIERARCHY.add_edge("PARTICIPANT|ID", "FAMILY|ID", MANY_MANY)
