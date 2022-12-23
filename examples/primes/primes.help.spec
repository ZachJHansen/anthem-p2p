# lemma "aa"
lemma: forall X, N1, N2 ( (N1 > 1 and N2 > 1 and X = N1 * N2) -> (N1 <= X and N2 <= X) ).

# Break spec into 2 directions:
# spec: forall X (prime(X) <-> exists N1 (exists N2 (N2 = n and 2 <= N1 and N1 <= N2) and not composite_1(N1) and X = N1))
# this direction is easier and does not require any additional lemmas
lemma:  forall X (prime(X) <-  exists N1 (exists N2 (N2 = n and 2 <= N1 and N1 <= N2) and not composite_1(N1) and X = N1)).
# this direction is harder (is sped up by including lemma "aa" above)
lemma:  forall X (prime(X)  -> exists N1 (exists N2 (N2 = n and 2 <= N1 and N1 <= N2) and not composite_1(N1) and X = N1)).

