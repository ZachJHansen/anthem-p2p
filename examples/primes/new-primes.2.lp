composite_2(I*J) :- I = 2..n, J = 2..n.
prime(I) :- I = 2..n, not composite_2(I).
