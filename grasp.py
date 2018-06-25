import sys
import numpy as np
import math
import random
import itertools
import datetime
import time as cronometro
import os


INTERACTIONS = 25000


INSTANCIA_TESTE = '/home/gabriel/git/biggest-min-dist-selection-grasp/instances/mdmt39.112.A.ins'
SOLUCOES_GULOSAS = 0
PROBABILITY = 0.20




def get_time_reference():
    time = datetime.datetime.now()
    day, hours = str(time).split()
    day = day.split('-')
    hours = hours.split(':')
    start = cronometro.time()
    return time, day, hours, start



def grasp(D, M, L, l, interactions):
    #Aplica a meta-heurística GRASP para resolver o problema

    
    time, day, hours, start = get_time_reference()
    print("Started grasp! {}-{}-{}-{}".format(hours[0], hours[1], day[2], day[1]))
    open('results/{}-{}-{}-{}.txt'.format(hours[0], hours[1], day[2], day[1]), 'w').close()

    d = []
    for e in range(L):
        d.append(evaluate_candidate(e,D))



    last_100 = [0 for _ in range(100)]
    

    c_interaction = 0

    if interactions > 0:
        best_solution = []
        best_value = 0

        for k in range(interactions):
            p_solution, p_value = random_greedy(D, M, L, l, PROBABILITY, d)
            p_solution, p_value = local_search(p_solution, D ,M, L, l)
            if p_value > best_value:
                best_solution = p_solution[:] 
                best_value = p_value
            c_interaction += 1
            
    
            last_100.append("{} & {} & {} \n".format(c_interaction,best_value, best_solution))
            last_100.pop(0)
            print("Iteraction {} - best value: {} - execution time: {}".format(c_interaction, best_value, int(cronometro.time() - start) ))
            if c_interaction % 1 == 900:
                print("Iteraction {} - best value: {} - execution time: {}".format(c_interaction, best_value, int(cronometro.time() - start) ))
                f = open('results/{}-{}-{}-{}.txt'.format(hours[0], hours[1], day[2], day[1]), 'a')
                for res in last_100:
                    f.write(res)
                count = 0

       


        return best_solution, best_value
    else:
        raise Exception

def value(solution, D, M):
    # Returns the value of a solutionm

    sol = []
    for m in range(M):
        sol.append(min_ml(m, solution, D))
    return sum(sol)

def random_greedy(D, M, L, l, e, d):

    # começa com um conjunto vazio
    S = set()
    # inicializa o conjunto de canditos: C ← E;
    C = set([x for x in range(L)])

    evaluation = [tuple([x, d[x]]) for x in C]
    evaluation.sort(key=lambda tup : tup[1], reverse=True)

    while len(S) < l:

        
        
        # Select an element s ∈ C with the biggest distance; 
        max_index = int(abs(len(C)*e)) 
        # Select the a candidate from the resticted list
        index = random.randint(0, len(C)-1)
        s = evaluation[index][0]
        S.add(s)
        C = C - set([s])

        evaluation.pop(index)

    S = list(S)
    return S, value(S, D, M)


def generate_neighbors(S, D, M, L, l):

    print("Tamanho da solução:")
    print(len(set(S)))

    # Gerando os vizinhos
    current = set(S)
    possibilities = set([x for x in range(l)])
    
    # print(len(current), len(possibilities))

    dif = possibilities - current
    dif = list(dif)
    current = list(current)

    # agora, para cada um dos valores utilizados em na solução atual, devo fazer a troca com cada um dos valores da diferença
    # esse processo custará len(solution)*(len(possibilities)-len(solution))

    neighbors = []
    for i in range(len(current)):
        for j in range(len(dif)):
            n = current[:]
            n[i] = dif[j]
            neighbors.append(n)
    print("Num of neighbors:  {} ".format(len(neighbors)))

    # aqui temos os vizinhos, precisamos medir suas qualidades

    neighbors_and_quality = []
    for neighbor in neighbors:
        neighbors_and_quality.append(tuple([neighbor, value(neighbor, D, M)]))

    return neighbors_and_quality

    


def local_search(solution, D, M, L, l):
    # apply local search generating

    s = solution[:]
    s_val = value(s, D, M)
    while True:
        n = generate_neighbors(s, D, M, L, l)
       
        index_max = np.argmax(x[1] for x in n)
        s_tuple = n[index_max]
        s_ = s_tuple[0][:]
        s_value = s_tuple[1]
        
        if s_val < s_value:
            s = s_[:]
            s_val = s_value
            
        else:
            break
    return s, s_value



    
def parse_instance(inst):

    file = open(inst,'r')
    instance = [abs(float(x)) for x in file.read().split()]
    file.close()
 
    M = int(instance[0]) 
    L = int(instance[1]) 
    l = int(instance[2])

    print("|M|: {}, |L|: {}, l: {}".format(M,L,l))

    D = np.zeros((M,L), int)

    i = 0
    for k in range(3,(M*L)+3):
        j = (k-3)%L

        D[(i,j)] = instance[k]
        if j == L-1:
            i+=1 

    return M, L, l, D


def read_all_stdin():
    content = ""
    for line in sys.stdin:
        content+=' ' + line
    return content.split()


def evaluate_candidate(e, D):
    M, L = D.shape
  
    for m in range(M):
        max_value = 0
        if D[m,e] > max_value:
            max_value = D[m,e]
    return max_value

def min_ml(m,S, D):
    min_dist = 9999
    for s in S: 
        e = D[m,s]
        if e < min_dist:
            min_dist = e
    return min_dist

def main():

    # D é a matriz de adjacência com os valores dos pesos
    M, L, l, D = parse_instance(INSTANCIA_TESTE)
    
    print(D)
    S, value = grasp(D, M, L, l, INTERACTIONS)
    print("Best solution quality: {} \n Agent: \n {}".format(value, S))
    


if __name__ == "__main__":
    main()