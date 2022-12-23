three(N) :- N = 1..n, I = 0..n, J = 0..n, K = 0..n, N = I*I+J*J+K*K.
more_than_three(N) :- N = 1..n, not three(N).

