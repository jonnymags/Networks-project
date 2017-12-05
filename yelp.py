import networkx as nx
import json
import matplotlib.pyplot as plt
import sys
from collections import defaultdict
from networkx.algorithms import bipartite
import numpy as np
import mmsbm
import time

def parse_reviews(review_file, business_ids):
	user_ids = []
	reviews = defaultdict(list)
	stars = {}
	i = 0

	with open(review_file, "r") as f:
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
	with open(business_file, "r") as f:
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
	
	
	b0 = 0 
	b1 = 0
	for node in b.nodes():
		b.node[node]['eta-theta'] = np.full(10,0.1)
		if b.node[node]['bipartite'] == 0:
			b0 += 1
		if b.node[node]['bipartite'] == 1:
			b1 += 1
	print(b0,b1,b0+b1,len(b.nodes()))

	p = np.full((5,10,10), 0.2) ## (r,k,l)

	#for edge in b.edges():
	#	print(stars[mmsbm.order_edge(b,edge)])

	t1 = time.time()
	for i in range(5):
		mmsbm.update(b,p,stars)
		t2 = time.time()
		print(t2-t1)
	print(b.nodes(data=True))
	for r in range(5):
		print(p[r])
	'''
	count = 0
	nodes = nx.get_node_attributes(b,'bipartite')
	print(nodes)
	for att in nodes:
		if nodes[att] == 0:# print(att)# == 1:
			count += 1
			G.node[
	'''
	#print(count)
	#print(stars[('ajxohdcsKhRGFlEvHZDyTw', 'PSMJesRmIDmust2MUw7aQA')])
#	nx.draw(b)
#	plt.show()

	#print(len(user_ids))

if __name__ == "__main__":
	main()
