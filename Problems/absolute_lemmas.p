# The axioms encoding standard interpretations are added to every ANTHEM theory.
# The following lemmas are all consequences of those axioms, some are useful for certain verification tasks.
# This could become a standard file containing such lemmas with names/labels, and allow the user to give Vampire advice of the form “Use Lemma so-and-so.”


# Lemma 1: Originally developed for Primes problem
# forall X, N1, N2 ( (N1 > 1 and N2 > 1 and X = N1 * N2) -> (N1 <= X and N2 <= X) ).

tff(absolute_lemma_1, axiom, ![X: object, N1: $int, N2: $int]: ((($greater(N1, 1) & $greater(N2, 1) & X = f__integer__($product(N1, N2))) => (p__less_equal__(f__integer__(N1), X) & p__less_equal__(f__integer__(N2), X))))).


# Another thing that seems to accelerate proof search is dividing an equivalence conjecture into two implication conjectures.
# It could be that future versions of ANTHEM should always divide completions and other equivalences in this way.

