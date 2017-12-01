import networkx as nx
import json
import matplotlib.pyplot as plt
import sys
from collections import defaultdict
from networkx.algorithms import bipartite

def parse_reviews(review_file, business_ids):
	user_ids = []
	reviews = defaultdict(list)
	stars = {}
	i = 0

	with open(review_file, "rb") as f:
		for line in f:
			j = json.loads(line)
			business_id = j["business_id"]
			if business_id in business_ids:
				user_id = j["user_id"]
				user_ids.append(user_id)
				reviews[user_id].append(business_id)
				stars[(user_id, business_id)] = j["stars"]
				i += 1

	items = []
	for key in reviews:
		for val in reviews[key]:
			items.append((key, val))

	return items, user_ids, reviews, stars 


def parse_businesses(business_file):
	business_ids = {}
	i = 0
	with open(business_file, "rb") as f:
		for line in f:
			j = json.loads(line)
			if i < 100 and j["city"] == "Las Vegas" and "Food" in j["categories"]:
				business_ids[j["business_id"]] = 0
				i += 1

	return business_ids


def main():
	try:
		review_file = sys.argv[1]
		business_file = sys.argv[2]
	except IndexError as e:
		print("Must provide input file.")
		sys.exit(-1)

	business_ids = parse_businesses(business_file)
	items, user_ids, reviews, stars = parse_reviews(review_file, business_ids)

	b = nx.Graph()
	b.add_nodes_from(user_ids, bipartite=0)
	b.add_nodes_from(business_ids.keys(), bipartite=1)
	b.add_edges_from(items)
	nx.draw(b)
	plt.show()



if __name__ == "__main__":
	main()