import sys
import numpy as np
import math
import random
import itertools
import datetime
import time as cronometro
import os
from random import shuffle

import logging

from operator import itemgetter

# FILE_TO_BEST_SOLUTION ='results/la_cu_caratia.txt'
# ITERACTIONS = 10000
# NUM_VIZINHOS = 8
# SOLUCOES_GULOSAS = 100
# ALPHA = 0.1
# LOCAL_SEARCH_CRITERIA = 20


FILE_TO_BEST_SOLUTION ='results/la_cu_caratia.txt'
ITERACTIONS = 10000
NUM_VIZINHOS = 100
SOLUCOES_GULOSAS = 100
ALPHA = 0.1
LOCAL_SEARCH_CRITERIA = 1


INSTANCIA_TESTE = '/home/gabriel/git/biggest-min-dist-selection-grasp/instances/mdmt39.112.A.ins'





#python3 ngrasp.py <FILE_TO_BEST_SOLUTION> <ITERACTIONS_GRASP> <NUM_VIZINHOS> <SOLUCOES_GULOSAS> <ALPHA> <LOCAL_SEARCH_CRITERIA>

# -------- ----------GRASP --------- ---------------
def grasp(d, l):

    start = cronometro.time()

    #-------------------------------LOGS-----------------------------------------------------
    logging.basicConfig(filename='results/'+str(datetime.datetime.now()),level=logging.DEBUG)
    logging.info("GRASP ITERATIONS: {} ".format(ITERACTIONS))
    logging.info("Instância: {} ".format(INSTANCIA_TESTE))
    logging.info("SOLUCOES_GULOSAS: {} ".format(SOLUCOES_GULOSAS))
    logging.info("ALPHA: {} ".format(ALPHA))
    logging.info("LOCAL_SEARCH_CRITERIA: {} ".format(LOCAL_SEARCH_CRITERIA))
    logging.info("NUM_VIZINHOS: {} ".format(NUM_VIZINHOS))
    #-----------------------------------------------------------------------------------------

   
    f = 0
    S = []
    for it in range(ITERACTIONS):
        s = greedy_randomized(d, l, ALPHA)
        s = local_search(s, l, d)
        f_ = evaluate(s, d)
        if f_ > f:
            f = f_
            S[:] = s[:]
        print("it. {}: bv: {} - seconds: {}".format(it, f, int(cronometro.time()-start)))
        logging.info('{} - {} - {}'.format(it, f, int(cronometro.time()-start)))

    logging.info("TOTAL TIME: {} ".format(int(cronometro.time()-start)))
    return S, f


# --------------------------------------------------
# ----------- Início guloso Randomizado ------------

def greedy_randomized(d, l, alpha):
    """Gera solução inicial """

    M,L = d.shape
   
    list_of_solutions = []

    l_elements = [x for x in range(L)]
    for it in range(SOLUCOES_GULOSAS):
        shuffle(l_elements)
        s = l_elements[:l] 
        f = evaluate(s, d)       
        list_of_solutions.append([f, s])

    # # # while len(list_of_solutions) < SOLUCOES_GULOSAS:
    # # #     shuffle(l_elements)
    # # #     s = l_elements[:l]
    # # #     f = evaluate(s, d)
    # # #     if f > best: 
    # # #         best = f
    # # #         best_sol = s[:]
    # # #         list_of_solutions.append([best, best_sol])
            
    index_max = int(math.floor(len(list_of_solutions)*alpha))
   
    rlc = sorted(list_of_solutions, key=itemgetter(0), reverse=True)[:index_max]
   
    index_solution = random.randint(0, len(rlc)-1) 
    best_sol = rlc[index_solution][1]

    return best_sol

# ------------------------------------------------
# ----------- Busca local  ------------

def local_search(S, l, d):
    """ Aplica uma busca local com NUM_VIZINHOS vizinhos """

    _, L = d.shape

    best_sol = []
    best_sol_value = 0

    for it in range(LOCAL_SEARCH_CRITERIA):
        S_ = []
        S_ [:] = S[:]
        f = evaluate(S_,d)

        N = generate_neighbors(S_, L)
        best_neighbor = N[np.argmax([evaluate(x, d) for x in N])]
        bn_value = evaluate(best_neighbor, d)

        while bn_value > f:
    
            f = bn_value
            S_[:] = best_neighbor[:]

            N[:] = generate_neighbors(S_, L)
            best_neighbor[:] = N[np.argmax([evaluate(x, d) for x in N])].copy()
            
            bn_value = evaluate(best_neighbor, d)
        if f > best_sol_value:
            best_sol[:] = S_[:]
            best_sol_value = f


    return best_sol






# ----------- Geração dos vizinhos   -------------

def generate_neighbors(S,L):

    S_ = S[:]
    
    N = []
    while len(N) < NUM_VIZINHOS:
        index = random.randint(0,len(S_)-1)
        n = random.randint(0,L-1)
        while n in S_:
            n = random.randint(0,L-1)
        if (n >= 450):
            break
        S_[index] = n
        N.append(S_)
    return N 


# ------------------------------------------------
# ---------- Função objetivo ---------------------

def evaluate(S, d):
    """Função objetivo"""
    M, L = d.shape
    result = 0
    for m in range(M):
        dm = math.inf
        for e in S:
            dm = min(dm, d[m,e])
        result += dm
    return result

# ------------------------------------------------
# ----------- Parser para a entrada  ------------

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

            
def main():
    

    # D é a matriz de adjacência com os valores dos pesos
    M, L, l, d = parse_instance(INSTANCIA_TESTE)
    
    best_sol, best_value = grasp(d, l)
    print("Best solution quality: {} \n Agent: \n {}".format(best_value, best_sol))
    logging.info("Best solution quality: {} \n Agent: \n {}".format(best_value, best_sol))
    

    f=open(BEST)


if __name__ == "__main__":
    main()
