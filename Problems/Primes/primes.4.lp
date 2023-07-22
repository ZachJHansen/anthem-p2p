sqrt_b(M) :- M = 1..b, M*M <= b, (M+1)*(M+1) > b.
composite(I*J) :- sqrt_b(M), I = 2..M, J = 2..b, I <= J.
prime(I) :- I = a..b, not composite(I).