composite(I*J) :- I > 1, J > 1.
prime(I) :- I = a..b, not composite(I).
