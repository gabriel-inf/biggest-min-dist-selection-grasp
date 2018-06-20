def grasp(G, l, stop_criteria) -> list():
    while True:
        s_ = random_greedy(G, l, alpha)
        s_ = localSearch(G, s_)
        if evaluate(s_) > evaluete(s):
            s = s_[:]

        iterations += 1
        if iterations >= stop_criteria:
            break

def random_greedy(G, l , e):
    # build a solution based in e-greedy strategy
    i = 0
    while 
