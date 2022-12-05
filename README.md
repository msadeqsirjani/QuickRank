# Page Rank Algorithm and Implementation

PageRank (PR) is an algorithm used by Google Search to rank websites in their search engine results. PageRank was named after Larry Page, one of the founders of Google. PageRank is a way of measuring the importance of website pages. According to Google:

* PageRank works by counting the number and quality of links to a page to determine a rough estimate of how important the   website is. The underlying assumption is that more important websites are likely to receive more links from other websites.

It is not the only algorithm used by Google to order search engine results, but it is the first algorithm that was used by the company, and it is the best-known.
The above centrality measure is not implemented for multi-graphs.

## Algorithm 
The PageRank algorithm outputs a probability distribution used to represent the likelihood that a person randomly clicking on links will arrive at any particular page. PageRank can be calculated for collections of documents of any size. It is assumed in several research papers that the distribution is evenly divided among all documents in the collection at the beginning of the computational process. The PageRank computations require several passes, called “iterations”, through the collection to adjust approximate PageRank values to more closely reflect the theoretical true value.

## Simplified algorithm 
Assume a small universe of four web pages: A, B, C, and D. Links from a page to itself, or multiple outbound links from one single page to another single page, are ignored. PageRank is initialized to the same value for all pages. In the original form of PageRank, the sum of PageRank over all pages was the total number of pages on the web at that time, so each page in this example would have an initial value of 1. However, later versions of PageRank, and the remainder of this section, assume a probability distribution between 0 and 1. Hence the initial value for each page in this example is 0.25.
The PageRank transferred from a given page to the targets of its outbound links upon the next iteration is divided equally among all outbound links.
If the only links in the system were from pages B, C, and D to A, each link would transfer 0.25 PageRank to A upon the next iteration, for a total of 0.75.

```python
PR(A) = PR(B) + PR(C) + PR(D)
```

Suppose instead that page B had a link to pages C and A, page C had a link to page A, and page D had links to all three pages. Thus, upon the first iteration, page B would transfer half of its existing value, or 0.125, to page A and the other half, or 0.125, to page C. Page C would transfer all of its existing value, 0.25, to the only page it links to, A. Since D had three outbound links, it would transfer one-third of its existing value, or approximately 0.083, to A. At the completion of this iteration, page A will have a PageRank of approximately 0.458. 

```python
PR(A) = PR(B) / 2 + PR(C) / 1 + PR(D) / 3
```

In other words, the PageRank conferred by an outbound link is equal to the document’s own PageRank score divided by the number of outbound links L( ).

```python
PR(A) = PR(B) / L(B) + PR(C) / L(C) + PR(D) / L(D)
```
In the general case, the PageRank value for any page u can be expressed as:

```python
PR(A) = Σ PR(v) / L(v)
```

i.e. the PageRank value for a page u is dependent on the PageRank values for each page v contained in the set Bu (the set containing all pages linking to page u), divided by the number L(v) of links from page v. The algorithm involves a damping factor for the calculation of the PageRank. It is like the income tax which the govt extracts from one despite paying him itself.

```python
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
            print(f"#{i} => [Node: {node} / Page-Rank: {pr}]")


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
    page_ranks[starting_node] = pr
    return pr
```