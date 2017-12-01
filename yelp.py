import networkx as nx
import json
import matplotlib.pyplot as plt
import sys
from collections import defaultdict

from networkx.algorithms import bipartite

def main():
	try:
		review_file = sys.argv[1]
	except IndexError as e:
		print("Must provide input file.")
		sys.exit(-1)

	user_ids = []
	business_ids = []
	reviews = defaultdict(list)
	stars = {}
	i = 0
	with open(review_file, "rb") as f:
		for line in f:
			if i < 100:
				j = json.loads(line)
				uid = j["user_id"]
				bid = j["business_id"]

				user_ids.append(uid)
				business_ids.append(bid)
				reviews[uid].append(bid)
				stars[(uid, bid)] = j["stars"]
				i += 1
			else:
				break

	#items = reviews.items()
	items = []
	for key in reviews:
		for val in reviews[key]:
			items.append((key, val))
			
	print(items)
	b = nx.Graph()
	b.add_nodes_from(user_ids, bipartite=0)
	b.add_nodes_from(business_ids, bipartite=1)
	b.add_edges_from(items)
	nx.draw(b)
	plt.show()



if __name__ == "__main__":
	main()