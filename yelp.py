import networkx as nx
import json
import matplotlib.pyplot as plt
import sys
from collections import defaultdict
from networkx.algorithms import bipartite
import numpy as np
import mmsbm
import time
import pickle

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
	print(len(user_ids))
	return items, user_ids, reviews, stars 



def parse_reviews_training(review_file, business_ids):
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
	

	## shuffle items
	rand_items = np.random.permutation(items)
	
	## make train and test sets
	training_items = rand_items[:int(len(rand_items)*.80)]
	test_items = rand_items[int(len(rand_items)*.80):]
	
	u_set = set(user_ids)
	training_set = set()
	for edge in training_items:
		training_set.add(edge[0])
		training_set.add(edge[1])
	training_set.intersection_update(u_set)

	test_set = set()
	for edge in test_items:
		test_set.add(edge[0])
		test_set.add(edge[1])
	test_set.intersection_update(u_set)

	b_set = set(business_ids.keys())
	b_training_set = set()
	for edge in training_items:
		b_training_set.add(edge[0])
		b_training_set.add(edge[1])
	b_training_set.intersection_update(b_set)

	print(len(b_training_set),len(b_set))

	return items, user_ids, reviews, stars, training_items, test_items, list(training_set), list(test_set), list(b_training_set)





def parse_businesses(business_file):
	business_ids = {}
	i = 0
	with open(business_file, "r") as f:
		for line in f:
			j = json.loads(line)
			#if i < 100 and j["city"] == "Las Vegas" and "Food" in j["categories"]:
			if j["city"] == "Las Vegas" and "Food" in j["categories"]:
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

	#items, user_ids, reviews, stars, training_items, test_items, training_ids, test_ids, training_business_ids= parse_reviews_training(review_file, business_ids)
	items, user_ids, reviews, stars = parse_reviews(review_file, business_ids)

	rating = np.zeros(5)

	print(len(stars))
	for key in stars:
		rating[stars[key]-1] += 1
	print(rating)
	'''
	b = nx.Graph()
	b.add_nodes_from(user_ids, bipartite=0)
	b.add_nodes_from(business_ids.keys(), bipartite=1)
	b.add_edges_from(items)
	print(len(user_ids), len(business_ids), len(items))
	for node in b.nodes():
		if 
	'''
	'''
	b = nx.Graph()
	b.add_nodes_from(training_ids, bipartite=0)
	b.add_nodes_from(training_business_ids, bipartite=1)
	b.add_edges_from(training_items)
	'''
	b0 = 0 
	b1 = 0
	for node in b.nodes():
		b.node[node]['eta-theta'] = np.random.dirichlet(np.ones(10),1)[0]
		if b.node[node]['bipartite'] == 0:
			b0 += 1
		if b.node[node]['bipartite'] == 1:
			b1 += 1
	print(b0,b1,b0+b1,len(b.nodes()))

	p = np.full((5,10,10), 0.2) ## (r,k,l)

	for k in range(10):
		for l in range(10):
			vector = np.random.dirichlet(np.ones(5),1)[0]
			for r in range(5):
				p[r,k,l] = vector[r]


	#for edge in b.edges():
	#	print(stars[mmsbm.order_edge(b,edge)])


	#for r in range(5):
	#	print(p[r])
	
	pickle.dump(items,open("items.p","wb"))
	pickle.dump(business_ids,open("business_ids.p","wb"))
	'''
	pickle.dump(user_ids.p,open("user_ids.p","wb"))
	pickle.dump(stars,open("reviews.p","wb"))
	pickle.dump(stars,open("stars.p","wb"))
	pickle.dump(stars,open("training_items.p","wb"))
	pickle.dump(stars,open("test_items.p","wb"))
	pickle.dump(stars,open("training_ids.p","wb"))
	pickle.dump(stars,open("test_ids.p","wb"))
	pickle.dump(stars,open("pOG.p","wb"))
	pickle.dump(stars,open("bOG.p","wb"))
	for i in range(1,26):
		t1 = time.time()
		mmsbm.update(b,p,stars)
		t2 = time.time()
		print(t2-t1)
		print(b.node['LDfEWQRx2_Ijv_GyD38Abg']['eta-theta'])
		if i%5 == 0:
			pickle.dump(b,open("b80_"+str(i)+".p","wb"))
			pickle.dump(p,open("p80_"+str(i)+".p","wb"))
	'''
	#print(b.nodes(data=True))
	
	#for r in range(5):
	#	print(p[r])

	

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
