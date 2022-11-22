three(N) :- N = I*I+J*J+K*K.
more_than_three(N) :- N = 1..n, not three(N).

