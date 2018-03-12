from __future__ import division
from itertools import product, combinations, permutations
import math



"""Let's choose n = 3 variables, x0, x1, x2. So we also have y0, y1, y2
where yi is defined as NOT xi.

The search space X contains 2**3 = 8 points.

There are then 6 literals, so (6 choose 2) = 15 possible clauses.

Any formula phi must consist of some subset of these clauses, so the
number of possible formulae is 2**15 = 32768.

Another way of counting is: for m = 0 clauses, there is 1 possible
fitness value (0); for m > 1 there are m+1 possible fitness values (0,
1, ... m); there may be some special cases eg for m = 15, phi will
include all possible clauses, and some will be incompatible, so I
guess f(x) = 15 is never achieved. Enumerate these to check. But for a
first pass, say that for m clauses, we have m+1 possible fitness
values, hence 8**(m+1) possible fitness functions.

For m clauses, we have (15 choose m) possible formulae.

Let's save all the formulae and all the tables that we achieve

And also create the dictionaries mapping formula <-> fitness table, eg

[(x0, y1), (x1, y2)] <-> [0, 1, 0, 2, 2, 2, 0, 1]

Then for each table, we try all its permutations until we find one
that is not reachable using any formula.

"""







# choose = lambda N, k: int(scipy.misc.comb(N, k))
#
# from https://stackoverflow.com/a/4941846
# I'm using this because I want to avoid import scipy,
# because I want to run pypy.
def choose(n,r):
    f = math.factorial
    return f(n) // f(r) // f(n-r)


def make_fit(phi):
    """Make the fitness function corresponding to "target" formula phi.
    Fitness is defined as the number of clauses in phi satisfied
    by the candidate solution x, a bitstring.

    phi will be a string of the form "[(x[0], y[1]), (x[1], y[2])]"

    >>> make_fit("[(x[0], y[1]), (x[1], y[2])]")([0, 0, 0])
    2
    >>> make_fit("[(x[0], y[1]), (x[1], y[2])]")([1, 1, 1])
    2

    """

    def fitness(x):
        y = [not xi for xi in x]
        phi_ = eval(phi)
        return sum((a or b) for a, b in phi_)

    return fitness

def fit_table(phi, n):
    # Given a "target" formula phi, make a table of the fitness values
    # of all bitstrings in the search space (bitstrings of length n)
    # ordered by the natural ordering of bitstrings.
    f = make_fit(phi)
    return tuple([f(x) for x in product([0, 1], repeat=n)])

def enum_formulae(n, m=None):
    # generate all possible formulae. A formula is a disjunction
    # (OR-ed) of clauses. A clause is a pair of literals AND-ed. A
    # literal is a variable or a negated variable.
    #
    # enum_formula(n, m) yields all formulae on n variables composed
    # of exactly m conjunctions.
    #
    # enum_formula(n) yields all formulae on n variables of any number
    # of conjunctions (but for given n, only 2n choose 2 possible
    # clauses exist).
    varnames = ["x[%d]" % i for i in range(n)] + ["y[%d]" % i for i in range(n)]
    if m is None:
        nclauses = choose(2 * n, 2)
        for m in range(1, nclauses + 1):
            # print(m)
            yield from enum_formulae(n, m)
    else:
        clauses = ["(%s, %s)" % (a, b) for a, b in combinations(varnames, 2)]
        formulae = ["[" + ", ".join(comb) + "]" for comb in combinations(clauses, m)]
        yield from formulae


def search_for_unreachable(fit_tables, fit_tables_to_formulae):
    # given a list of fitness tables, and a mapping from tables to
    # formulae, find a fitness table which occurs as a permutation of
    # an existing fitness table but does not occur ("is not
    # reachable") as the fitness table of any formula.
    for i, table in enumerate(fit_tables):
        print(str(i) + " of " + str(len(fit_tables)))
        print(table)
        print(fit_tables_to_formulae[table])
        for perm in permutations(table):
            if perm not in fit_tables:
                yield table, perm


def run(n):
    
    print("n: ", n)
    fit_tables = []
    formulae = []
    fit_tables_to_formulae = dict()
    #formulae_to_fit_tables = dict()
    nformulae = sum(1 for x in enum_formulae(n))
    
    for i, phi in enumerate(enum_formulae(n)):
        #f = make_fit(phi)
        table = fit_table(phi, n)        
        fit_tables.append(table)
        formulae.append(phi)
        fit_tables_to_formulae[table] = phi
        #formulae_to_fit_tables[phi] = table

        if i % 1000 == 0:
            print("nformulae: " + str(i) + " of " + str(nformulae) + "; phi: " + phi + ": " + str(table))

    print("Number of fitness tables: ", len(fit_tables_to_formulae))
    print("Number of formulae: ", nformulae)

    for table, perm in search_for_unreachable(fit_tables, fit_tables_to_formulae):
        print("Table " + "".join(map(str, table)) + " is reachable")
        print("by formula " + str(fit_tables_to_formulae[table]))
        print("but its permutation " + "".join(map(str, perm)) + " is not")
        break
    else:
        print("all permutations of all fitness tables were reachable")



# trying this for n=4 is already very slow on my desktop -- pypy may
# help.  but we could optimise code and maybe remove one of the dicts,
# without affecting results, to save a lot of memory.
run(3) 



"""
Results:


n:  2
Number of fitness tables:  47
Number of formulae:  63
all permutations of all fitness tables were reachable


n:  3
Number of fitness tables:  9922
Number of formulae:  32767
0 of 32767
(0, 0, 1, 1, 1, 1, 1, 1)
[(x[0], x[1])]
Table 00111111 is reachable
by formula [(x[0], x[1])]
but its permutation 01101111 is not


"""
