import sys
import numpy as np
import math
import random
import itertools
import datetime
import time as cronometro



INTERACTIONS = 25000


INSTANCIA_TESTE = '/home/gabriel/git/biggest-min-dist-selection-grasp/instances/mdmt39.112.A.ins'
SOLUCOES_GULOSAS = 0
PROBABILITY = 0.20




def grasp(D, min_dists, M, L, l, interactions):
    #Aplica a meta-heurística GRASP para resolver o problema

    

    time = datetime.datetime.now()
    day, hours = str(time).split()
    day = day.split('-')
    hours = hours.split(':')

    start = cronometro.time()

    print("Started grasp! {}-{}-{}-{}".format(hours[0], hours[1], day[2], day[1]))


    # clear the thing
    open('results/{}-{}-{}-{}.txt'.format(hours[0], hours[1], day[2], day[1]), 'w').close()


    last_100 = [0 for _ in range(100)]
    count = 0

    c_interaction = 0

    if interactions > 0:
        best_solution, best_value = random_greedy(D, M, min_dists, L, l, PROBABILITY)
        best_solution, best_value = local_search(best_solution,D,min_dists , M, L, l)

        for k in range(interactions):
            p_solution, p_value = random_greedy(D, M, min_dists, L, l, PROBABILITY)
            p_solution, p_value = local_search(p_solution, D,min_dists ,M, L, l)
            if p_value > best_value:
                best_solution = p_solution[:] 
                best_value = p_value
            c_interaction += 1
            
    
            last_100.append("{} & {} & {} \n".format(c_interaction,best_value, best_solution))
            last_100.pop(0)
            print("Iteraction {} - best value: {} - execution time: {}".format(c_interaction, best_value, int(cronometro.time() - start) ))
            if count == 99:
                print("Iteraction {} - best value: {} - execution time: {}".format(c_interaction, best_value, int(cronometro.time() - start) ))
                f = open('results/{}-{}-{}-{}.txt'.format(hours[0], hours[1], day[2], day[1]), 'a')
                for res in last_100:
                    f.write(res)
                count = 0

            count += 1


        return best_solution, best_value
    else:
        raise Exception

def value(solution, D, M, min_dists):
    # Returns the value of a solutionm

    sol = []
    for e in solution:
        sol.append(min_dists[e])

    return sum(sol)

def update_candidates(n, L):
    C = set()
    while len(C) <  n:
        C.add(random.randint(0, L-1))
    return C


def random_greedy(D, M, min_dists, L, l, e):

    S = set()
    # Initialize the candidate set: C ← E;
    C = update_candidates(l,L)
  
    evaluation = [tuple([x,min_dists[x]]) for x in C]
    evaluation.sort(key=lambda tup : tup[1], reverse=True)

    while len(C) > 0:
        # Select an element s ∈ C with the biggest distance min_dists(s); 

        max_index = int(abs(len(C)*e))
        index = random.randint(0, len(C)-1)
        
        s = evaluation[index][0]
        S.add(s)
        C = update_candidates(len(C)-1, L)

        if len(C) > 0:
            evaluation = [tuple([x,min_dists[x]]) for x in C]
            evaluation.sort(key=lambda tup : tup[1], reverse=True)


    # # # # # # # build a solution based in e-greedy strategy
    # # # # # # S = []
    # # # # # # while len(S) < SOLUCOES_GULOSAS:
    # # # # # #     s = []
    # # # # # #     while len(s) < l:
    # # # # # #         # sorteia vértices de L que serão usados
    # # # # # #         new_number = random.randint(0, L-1)
    # # # # # #         if new_number not in s:
    # # # # # #             s.append(new_number)
    # # # # # #     S.append(tuple([s,value(s, D, M, min_dists)]))
    # # # # # # # ordena as soluções encontradas por qualidade
    # # # # # # S.sort(key=lambda tup : tup[1], reverse=True)

    # # # # # # # Formando a lista de melhores candidatos
    # # # # # # max_index = int(abs(len(S)*e))
    # # # # # # rlc = [s for s in S[0:max_index]]
    # # # # # # result = rlc[random.randint(0,max_index-1)]

    
    # retorna, de forma aleatoria um dos elementos da lista restrita e a qualidade obtida
    S = list(S)
    return S, value(S, D, M, min_dists)


def generate_neighbors(solution, D, min_dists, M, L, l):
    # gera os vizinhos para o local_search

    neighbors = []
    # Gerando os vizinhos
    current = set(solution)
    possibilities = set([x for x in range(l)])
    
    # print(len(current), len(possibilities))


    dif = possibilities - current
    dif = list(dif)
    current = list(current)



    # agora, para cada um dos valores utilizados em na solução atual, devo fazer a troca com cada um dos valores da diferença
    # esse processo custará len(solution)*(len(possibilities)-len(solution))

    for i in range(len(current)):
        for j in range(len(dif)):
            n = current[:]
            n[i] = dif[j]
            neighbors.append(n)
        
    # aqui temos os vizinhos, precisamos medir suas qualidades

    neighbors_and_quality = []
    for neighbor in neighbors:
        neighbors_and_quality.append(tuple([neighbor, value(neighbor, D, M, min_dists)]))

    return neighbors_and_quality

    


def local_search(solution, D, min_dists, M, L, l):
    # apply local search generating

    s = solution[:]
    s_val = value(s, D, M, min_dists)
    while True:
        n = generate_neighbors(s, D, min_dists, M, L, l)
       
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


def main():

    # D é a matriz de adjacência com os valores dos pesos
    M, L, l, D = parse_instance(INSTANCIA_TESTE)


    min_dists = []
    
    for j in range(L):
        min_temp = 999
        for m in range(M):
            n = D[m,j]
            if n < min_temp:
                min_temp = n
        min_dists.append(min_temp)


    
    S, value = grasp(D, min_dists, M, L, l, INTERACTIONS)

    print("Best solution quality: {} \n Agent: \n {}".format(value, S))
    


if __name__ == "__main__":
    main()