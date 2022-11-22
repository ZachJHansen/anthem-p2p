composite(I*J) :- I = 2..n, J = 2..n.
prime(I) :- I = 2..n, not composite(I).
