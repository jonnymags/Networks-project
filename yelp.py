import networkx as nx
import json
import matplotlib.pyplot as plt
import sys

from networkx.algorithms import bipartite


review_file = sys.argv[1]

def main():
	user_ids = []
	business_ids = []
	reviews = {}
	with open(review_file, "rb") as f:
		for line in f:
			j = json.loads(line)
			user_ids.append(j["user_id"])
			business_ids.append(j["business_id"])

			reviews[j["user_id"]] = j["business_id"]

	items = list(reviews.items())
	print(len(user_ids))
	b = nx.Graph()
	b.add_nodes_from(user_ids, bipartite=0)
	b.add_nodes_from(business_ids, bipartite=1)
	b.add_edges_from(items)


if __name__ == "__main__":
	main()