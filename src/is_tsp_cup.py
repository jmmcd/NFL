import sympy

"""A TSP problem is defined by a cost matrix C of size (n, n). A tour
is a permutation of the integers (1, ..., n). The cost of a tour is
the sum of the appropriate n elements from C.

For a tour such as (1, 2, 3, 4, 5, 6), we have:

f(1, 2, 3, 4, 5, 6) = C[1, 2] + C[2, 3] + C[3, 4] + C[4, 5] + C[5, 6] + C[6, 1]

Now, if TSP is *closed under permutation* (CUP) in the terms of the
sharpened No Free Lunch theorem, then we can permute the costs of
tours in any way we like, for example we can swap the costs of the
optimum and "pessimum" (?), and the resulting equations will still be
consistent with a TSP problem (potentially with a different cost
matrix C'). 

This code is intended to explore this. 


"""


# Consider the TSP problem with cost matrix:

"""
      $\begin{bmatrix}
        0 & 1 & 2 & 9 & 2 & 1 \\
        1 & 0 & 1 & 2 & 9 & 2 \\
        2 & 1 & 0 & 1 & 2 & 9 \\
        9 & 2 & 1 & 0 & 1 & 2 \\
        2 & 9 & 2 & 1 & 0 & 1 \\
        1 & 2 & 9 & 2 & 1 & 0
      \end{bmatrix}$
"""


# The following equations are just a few of the many which arise
C = sympy.symarray("C", (7, 7), nonnegative=True)
eqns = [
sympy.Eq(C[1][2] + C[2][3] + C[3][4] + C[4][5] + C[5][6] + C[6][1], 6),
sympy.Eq(C[1][2] + C[2][3] + C[3][4] + C[4][6] + C[6][5] + C[5][1], 8),
sympy.Eq(C[1][2] + C[2][3] + C[3][5] + C[5][4] + C[4][6] + C[6][1], 8),
sympy.Eq(C[1][2] + C[2][4] + C[4][3] + C[3][5] + C[5][6] + C[6][1], 8),
sympy.Eq(C[1][3] + C[3][2] + C[2][4] + C[4][5] + C[5][6] + C[6][1], 8),
sympy.Eq(C[1][3] + C[3][4] + C[4][5] + C[5][6] + C[6][2] + C[2][1], 8),
sympy.Eq(C[1][6] + C[6][2] + C[2][3] + C[3][4] + C[4][5] + C[5][1], 8)
]

# If we use sympy to solve, we find multiple solutions, one of which
# is the original C.
print("Solutions to equations from the original problem:")
print(sympy.solve(eqns))



# then permute the best and worst and show that it doesn't correspond
# to any cost matrix

C = sympy.symarray("C", (7, 7), nonnegative=True)
eqns = [
sympy.Eq(C[1][2] + C[2][3] + C[3][4] + C[4][5] + C[5][6] + C[6][1], 32),
sympy.Eq(C[1][2] + C[2][3] + C[3][4] + C[4][6] + C[6][5] + C[5][1], 8),
sympy.Eq(C[1][2] + C[2][3] + C[3][5] + C[5][4] + C[4][6] + C[6][1], 8),
sympy.Eq(C[1][2] + C[2][4] + C[4][3] + C[3][5] + C[5][6] + C[6][1], 8),
sympy.Eq(C[1][3] + C[3][2] + C[2][4] + C[4][5] + C[5][6] + C[6][1], 8),
sympy.Eq(C[1][3] + C[3][4] + C[4][5] + C[5][6] + C[6][2] + C[2][1], 8),
sympy.Eq(C[1][6] + C[6][2] + C[2][3] + C[3][4] + C[4][5] + C[5][1], 8)
]
print("Solutions to equations from the 'trap' construction:")
print(sympy.solve(eqns)) # [] -- no solution



# for ref, if we remove two of the equations, we do get a solution.
C = sympy.symarray("C", (7, 7), nonnegative=True)
eqns = [
sympy.Eq(C[1][2] + C[2][3] + C[3][4] + C[4][5] + C[5][6] + C[6][1], 6),
sympy.Eq(C[1][2] + C[2][3] + C[3][4] + C[4][6] + C[6][5] + C[5][1], 8),
sympy.Eq(C[1][2] + C[2][3] + C[3][5] + C[5][4] + C[4][6] + C[6][1], 8),
sympy.Eq(C[1][2] + C[2][4] + C[4][3] + C[3][5] + C[5][6] + C[6][1], 8),
sympy.Eq(C[1][3] + C[3][2] + C[2][4] + C[4][5] + C[5][6] + C[6][1], 8),
]
print("Solutions to a smaller set of equations from the 'trap' construction:")
print(sympy.solve(eqns))
# multiple solutions are possible -- this is just for curiosity -- how
# many of the equations have to be removed before we find a solution.



