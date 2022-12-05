TELEPORTATION = 0.15

networks = ["A", "B", "C"]

transitions_graph = [
    {"Key": "A", "Inputs": ["C"], "Outputs": ["B", "C"]},
    {"Key": "B", "Inputs": ["A"], "Outputs": ["C"]},
    {"Key": "C", "Inputs": ["B", "C"], "Outputs": ["A"]},
]

page_ranks = {"A": 1, "B": 1, "C": 1}


def search(list_of_dictionary, **kw):
    for value in filter(
        lambda i: all((i[k] == v for (k, v) in kw.items())), list_of_dictionary
    ):
        return value


def page_rank(
    networks: list,
    transitions_graph: list,
    teleportation: float = 0.15,
    max_iteration=100,
):
    for i in range(max_iteration):
        for node in networks:
            pr = estimate_probability(
                starting_node=node, networks=networks, transitions_graph=transitions_graph
            )
            print(f"#{i+1} => [Node: {node} / Page-Rank: {pr}]")


def estimate_probability(
    starting_node: str,
    networks: list,
    transitions_graph: list,
    teleportation: float = 0.15,
):
    related_nodes_sum = 0.0
    starting_transition_graph = search(transitions_graph, Key=starting_node)
    for node in starting_transition_graph["Inputs"]:
        other_transition_graph = search(transitions_graph, Key=node)
        output_nodes_length = len(other_transition_graph["Outputs"])
        related_nodes_sum = related_nodes_sum + page_ranks[node] / output_nodes_length

    pr = (teleportation / len(networks)) + (1 - teleportation) * related_nodes_sum
    # pr = 0.5 + 0.5 * related_nodes_sum
    page_ranks[starting_node] = pr
    return pr


if __name__ == "__main__":
    page_rank(
        networks=networks,
        transitions_graph=transitions_graph,
        teleportation=TELEPORTATION
    )
