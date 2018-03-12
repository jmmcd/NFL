import itertools
import numpy as np
import random

n = 2

# the "training set" is all possible 
X = np.array(list(itertools.product([False, True], repeat=n))).T

# a few example programs
def p0(X):
    return np.logical_and(X[0], X[1])
def p1(X):
    return np.logical_or(X[0], X[1])
def p2(X):
    return np.logical_not(X[0])
def p3(X):
    return np.logical_and(X[0], np.logical_not(X[1]))

# a search space consisting of three programs
p = [
    lambda X: np.logical_and(X[0], X[1]),
    lambda X: np.logical_or(X[0], X[1]),
    lambda X: np.logical_not(X[0]),
    # lambda X: np.logical_and(X[0], np.logical_not(X[1]))
]

def f(p, t, X):
    # fitness of a program p (given target semantics t) is Hamming distance
    s = p(X)
    return np.sum(t == s)

def match_all_fs(p, fs, X):
    # given a set of programs p and corresponding fitness values fs,
    # test whether there is any semantics s which would give those
    # fitness values to those programs. check by iterating over all
    # possible semantics s. If so, return the semantics. If not,
    # return None.
    for s in itertools.product([False, True], repeat=2**n):
        if all(f(pi, s, X) == fi for pi, fi in zip(p, fs)):
            return s
    return None

def all_p_match_permuted_fitness(p, t, X):
    # if we take a problem represented by a target semantics t, and
    # some programs in the search space, and permute its fitness
    # values, then do we get a new problem in the search space?  ie is
    # it CUP. check by trying all permutations of fitness values, and
    # for each trying all possible semantics.
    f_t_X = lambda p: f(p, t, X)
    fs = [f_t_X(pi) for pi in p]
    
    # for each permutation of the fitness values 
    for perm in itertools.permutations(fs):
        
        perm_str = ", ".join(map(lambda permi: str(int(permi)), perm))
        r = match_all_fs(p, perm, X)
        if r:
            print(perm_str, "can be matched, with: ", r)
        else:
            print(perm_str, "cannot be matched")
        print("")

t = (False, False, False, True) # just an example
print("target: ", t)
print("")
all_p_match_permuted_fitness(p, t, X)
