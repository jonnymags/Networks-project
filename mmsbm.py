import numpy as np

'''


def theta(g, u, k): # graph, user string, group int
    total = 0.0
    for edge in g.edges(u):
        #use edge[1]
        for l in range(10):
            total += omega(u,edge[1],k,l)
    return total / g.degree(u)

def eta(g, i, l): # graph, user string, group int
    total = 0.0
    for edge in g.edges(i):
        #use edge[1]
        for k in range(10):
            total += omega(edge[1],i,k,l) ##(u,i,k,l) 
    return total / g.degree(i)

def prob(g, k, l, r, stars): ## (graph, int, int, int, dict)
    den_sum = 0.0
    num_sum = 0.0
    for edge in g.edges():
        if stars[edge] == r:
            num_sum += omega(edge[0],edge[1],k,l)
        den_sum += omega(edge[0],edge[1],k,l)
    return num_sum / den_sum

def omega(g,u,i,k,l): ## (int, int, int, int)
    den_sum = 0.0
    for k_prime in range(10):
        for l_prime in range(10):
            den_sum += theta(g, u, k_prime) + eta(g, i, l_prime) + prob(g, k_prime, l_prime, r
'''

## stars {(userID, businessID) , rating} 
## users 0, business 1

def prac(test):
    test.add_edge(1,15)
    print('we done here')

def order_edge(b,edge): ##(graph, tuple)
    if b.node[edge[0]]['bipartite'] == 0:
        return (edge[0], edge[1])
    else:
        return (edge[1], edge[0])
    

def update(b,p,stars):

    omega_dict = {}
    ## build the omega dictionary, size is |edges| x |K| x |L|
    for edge in b.edges():
        ## o_edge is a tuple (userID, businessID) always
        o_edge = order_edge(b,edge)
        omega_dict[o_edge] = np.zeros((10,10))
        den_sum = 0.0
        for k in range(10):
            for l in range(10):
                theta = b.node[o_edge[0]]['eta-theta'][k]
                eta = b.node[o_edge[1]]['eta-theta'][l]
                p_prime = p[stars[o_edge]-1,k,l] ##remember to -1 for p
                omega_dict[o_edge][k,l] = theta * eta * p_prime
                den_sum += theta * eta * p_prime
        for k in range(10):
            for l in range(10):
                omega_dict[o_edge][k,l] /= den_sum
#    for key in omega_dict.keys():
#        print(omega_dict[key])
        

    ## update the theta, eta
    for node in b.nodes():
        ## update theta (user nodes only)
        if b.node[node]['bipartite'] == 0:
            for k in range(10):
                num_sum = 0.0
                for edge in b.edges(node): ## use edge[1] to find neighbor
                    o_edge = order_edge(b,edge)
                    for l in range(10):
                        num_sum += omega_dict[o_edge][k,l]
                b.node[node]['eta-theta'][k] = num_sum / b.degree(node) 
                #print(num_sum / b.degree(node))

        ## update eta (business nodes only)
        else:
            for l in range(10):
                num_sum = 0.0
                for edge in b.edges(node): ## use edge[1] to find neighbor
                    o_edge = order_edge(b,edge)
                    for k in range(10):
                        num_sum += omega_dict[o_edge][k,l]
                b.node[node]['eta-theta'][l] = num_sum / b.degree(node) 
                #print(num_sum / b.degree(node))




    ## update p
    for r in range(5):
        for k in range(10):
            for l in range(10):
                num = 0.0
                den = 0.0
                for edge in stars:
                    o_edge = order_edge(b,edge)
                    if stars[o_edge] == r+1:  
                        num += omega_dict[o_edge][k,l] ### PROBLEM edge order
                    den += omega_dict[o_edge][k,l]
                p[r,k,l] = num/den
                

#def main():


#if __name__ == "__main__":
#        main()
