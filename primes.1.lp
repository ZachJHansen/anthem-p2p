composite(I*J) :- I>1, J>1.
prime(I) :- I = 2..n, not composite(I).
