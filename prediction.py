import pickle
import numpy as np
import networkx as nx

def order_edge(edge, bids):
    if edge[0] in bids:
        return (edge[1],edge[0])
    else:
        return (edge[0],edge[1])



def main():
    b = pickle.load( open( "b80_25.p", "rb") )
    p = pickle.load( open( "p80_25.p", "rb") )
    items = pickle.load( open( "items.p", "rb") )
    business_ids = pickle.load( open( "business_ids.p", "rb") )
    stars = pickle.load( open( "stars.p", "rb") )
    preds = [0,0,0,0,0,0]
    for k in range(10):
        print(b.node["06o1DmiBoiyxI2q3v2QRbg"]['eta-theta'][k], end=" ")
    for node in b.nodes():
        if b.node[node]['bipartite'] == 1:
            Pr = np.zeros(5)
            for r in range(5):
                sum = 0.0
        
                for k in range(10):
                    for l in range(10):
                        theta = b.node["06o1DmiBoiyxI2q3v2QRbg"]['eta-theta'][k]
                        eta = b.node[node]['eta-theta'][l]

                        p_prime = p[r,k,l] 
                        sum += theta * eta * p_prime
                Pr[r] = sum

#            print(Pr)

            prediction = 0
            for i in range(5):
                if Pr[i] == max(Pr):
                    prediction = i+1
#            print(node, prediction) 
            preds[prediction] += 1
    print(preds)

    '''
    print(len(business_ids), len(items))
    print(len(stars.keys()))

    for r in range(5):
        for i in range(10):
            for j in range(10):
                print(p[r,i,j], end=" ")
            print("")
        print("")
    
    '''
    ## build the average theta and eta, for cold start
    ## user is theta is bipartite = 0
    ## restaurant is eta is bipartite = 1
    avg_theta = np.zeros(10)
    avg_eta = np.zeros(10)
    
    user_count = 0
    restaurant_count = 0

    for node in b.nodes():
        if b.node[node]['bipartite'] == 0:
            avg_theta += b.node[node]['eta-theta']
            user_count += 1
            #print(node, b.degree(node))
        else:
            avg_eta += b.node[node]['eta-theta']
            restaurant_count += 1

    
        
    

    avg_theta /= user_count
    avg_eta /= restaurant_count
    
    #print(test_ids)

    training_items = b.edges()
    test_items = []

    for edge in items:
        count = 0
        if edge in training_items:
            count += 1
        elif (edge[1],edge[0]) in training_items:
            count += 1
        else:
            test_items.append(edge)
    
    bids = business_ids.keys()
    
    cold_right = 0
    cold_wrong = 0
    right = 0
    wrong = 0
    whole_cold = 0
    half_cold = 0
    for edge in test_items:
        o_edge = order_edge(edge, bids)

        Pr = np.zeros(5)
        for r in range(5):
            sum = 0.0
        
            t_cold = False
            e_cold = False
            for k in range(10):
                for l in range(10):
                    theta = 0.0
                    eta = 0.0
                    
                    if o_edge[0] in b.nodes():
                        theta = b.node[o_edge[0]]['eta-theta'][k]
                    else:
                        theta = avg_theta[k]
                        t_cold = True
                    
                    if o_edge[1] in b.nodes():
                        eta = b.node[o_edge[1]]['eta-theta'][l]
                    else:
                        eta = avg_eta[l]
                        e_cold = True
                    p_prime = p[r,k,l] 
                    sum += theta * eta * p_prime
            Pr[r] = sum
        if t_cold and e_cold:
            whole_cold += 1
        elif t_cold or e_cold:
            half_cold += 1

        prediction = 0
        for i in range(5):
            if Pr[i] == max(Pr):
                prediction = i+1
             
        if prediction == stars[o_edge]:
            right += 1
            if t_cold or e_cold:
                cold_right += 1
        else:
            wrong += 1
            if t_cold or e_cold:
                cold_wrong += 1

    print( float(right) / (right + wrong) )
    print( whole_cold, half_cold, right, wrong, cold_right, cold_wrong)
    
#    print(len(training_items))
#    print(len(test_items))
#    print(len(items))

if __name__ == "__main__":
        main()
