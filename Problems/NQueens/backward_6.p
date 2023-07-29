%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% anthem types
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tff(type, type, object: $tType).
tff(type, type, f__integer__: ($int) > object).
tff(type, type, f__symbolic__: ($i) > object).
tff(type, type, c__infimum__: object).
tff(type, type, c__supremum__: object).
tff(type, type, p__is_integer__: (object) > $o).
tff(type, type, p__is_symbolic__: (object) > $o).
tff(type, type, p__less_equal__: (object * object) > $o).
tff(type, type, p__less__: (object * object) > $o).
tff(type, type, p__greater_equal__: (object * object) > $o).
tff(type, type, p__greater__: (object * object) > $o).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% anthem axioms
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tff(axiom, axiom, ![X: object]: (p__is_integer__(X) <=> (?[N: $int]: (X = f__integer__(N))))).
tff(axiom, axiom, ![X1: object]: (p__is_symbolic__(X1) <=> (?[X2: $i]: (X1 = f__symbolic__(X2))))).
tff(axiom, axiom, ![X: object]: ((X = c__infimum__) | p__is_integer__(X) | p__is_symbolic__(X) | (X = c__supremum__))).
tff(axiom, axiom, ![N1: $int, N2: $int]: ((f__integer__(N1) = f__integer__(N2)) <=> (N1 = N2))).
tff(axiom, axiom, ![S1: $i, S2: $i]: ((f__symbolic__(S1) = f__symbolic__(S2)) <=> (S1 = S2))).
tff(axiom, axiom, ![N1: $int, N2: $int]: (p__less_equal__(f__integer__(N1), f__integer__(N2)) <=> $lesseq(N1, N2))).
tff(axiom, axiom, ![X1: object, X2: object]: ((p__less_equal__(X1, X2) & p__less_equal__(X2, X1)) => (X1 = X2))).
tff(axiom, axiom, ![X1: object, X2: object, X3: object]: ((p__less_equal__(X1, X2) & p__less_equal__(X2, X3)) => p__less_equal__(X1, X3))).
tff(axiom, axiom, ![X1: object, X2: object]: (p__less_equal__(X1, X2) | p__less_equal__(X2, X1))).
tff(axiom, axiom, ![X1: object, X2: object]: (p__less__(X1, X2) <=> (p__less_equal__(X1, X2) & (X1 != X2)))).
tff(axiom, axiom, ![X1: object, X2: object]: (p__greater_equal__(X1, X2) <=> p__less_equal__(X2, X1))).
tff(axiom, axiom, ![X1: object, X2: object]: (p__greater__(X1, X2) <=> (p__less_equal__(X2, X1) & (X1 != X2)))).
tff(axiom, axiom, ![N: $int]: p__less__(c__infimum__, f__integer__(N))).
tff(axiom, axiom, ![N: $int, S: $i]: p__less__(f__integer__(N), f__symbolic__(S))).
tff(axiom, axiom, ![S: $i]: p__less__(f__symbolic__(S), c__supremum__)).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% types
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% predicate types
tff(type, type, q: (object) > $o).
tff(type, type, q: (object * object) > $o).
tff(type, type, q_1: (object) > $o).
% function types
tff(type, type, n: $int).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% assumptions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tff(statement_1, axiom, $greatereq(n, 1)).
tff(statement_2, axiom, ![X1: object]: (q_1(X1) <=> ?[X2: object]: (q(X1, X2)))).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% completed definitions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% completed definition of q/1
tff(completed_definition_q_1, axiom, ![X1: object]: (q(X1) <=> ?[X2: object]: (q(X1, X2)))).
% completed definition of q/2
tff(completed_definition_q_2, axiom, ![X1: object, X2: object]: (q(X1, X2) <=> (q(X1, X2) & ?[N1: $int]: (($lesseq(1, N1) & $lesseq(N1, n) & X1 = f__integer__(N1))) & ?[N2: $int]: (($lesseq(1, N2) & $lesseq(N2, n) & X2 = f__integer__(N2)))))).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% integrity constraints
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tff(integrity_constraint, axiom, ![X1: object, X2: object, X3: object]: (~(q(X1, X2) & q(X1, X3) & X2 != X3))).
tff(integrity_constraint, axiom, ![X1: object, X2: object, X3: object]: (~(q(X1, X2) & q(X3, X2) & X1 != X3))).
tff(integrity_constraint, axiom, ![X1: object, X2: object, X3: object, X4: object]: (~(q(X1, X2) & q(X3, X4) & p__less__(X1, X3) & ?[X5: object]: ((?[N1: $int, N2: $int]: ((X5 = f__integer__($difference(N1, N2)) & f__integer__(N1) = X1 & f__integer__(N2) = X3)) & ?[N3: $int, N4: $int]: ((X5 = f__integer__($difference(N3, N4)) & f__integer__(N3) = X2 & f__integer__(N4) = X4))))))).
tff(integrity_constraint, axiom, ![X1: object, X2: object, X3: object, X4: object]: (~(q(X1, X2) & q(X3, X4) & p__less__(X1, X3) & ?[X5: object]: ((?[N1: $int, N2: $int]: ((X5 = f__integer__($difference(N1, N2)) & f__integer__(N1) = X1 & f__integer__(N2) = X3)) & ?[N3: $int, N4: $int]: ((X5 = f__integer__($difference(N3, N4)) & f__integer__(N3) = X4 & f__integer__(N4) = X2))))))).
tff(integrity_constraint, conjecture, ![X: object]: (~(~q(X) & ?[N: $int]: (($lesseq(1, N) & $lesseq(N, n) & X = f__integer__(N)))))).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% specs
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tff(statement_1, axiom, ![X1: object, X2: object]: (q(X1, X2) <=> (q(X1, X2) & ?[N1: $int, N2: $int]: ((N1 = n & $lesseq(1, N2) & $lesseq(N2, N1) & X1 = f__integer__(N2))) & ?[N3: $int, N4: $int]: ((N3 = n & $lesseq(1, N4) & $lesseq(N4, N3) & X2 = f__integer__(N4)))))).
tff(statement_2, axiom, ![X1: object, X2: object, X3: object]: (~(q(X1, X2) & q(X1, X3) & X2 != X3))).
tff(statement_3, axiom, ![X1: object, X2: object, X3: object]: (~(q(X1, X2) & q(X3, X2) & X1 != X3))).
tff(statement_4, axiom, ![X1: object, X2: object, X3: object, X4: object]: (~(q(X1, X2) & q(X3, X4) & X1 != X3 & ?[X5: object]: ((?[N1: $int, N2: $int]: ((X5 = f__integer__($difference(N1, N2)) & f__integer__(N1) = X1 & f__integer__(N2) = X3)) & ?[N3: $int, N4: $int]: ((X5 = f__integer__($difference(N3, N4)) & f__integer__(N3) = X2 & f__integer__(N4) = X4))))))).
tff(statement_5, axiom, ![X1: object, X2: object, X3: object, X4: object]: (~(q(X1, X2) & q(X3, X4) & X1 != X3 & ?[X5: object]: ((?[N1: $int, N2: $int]: ((X5 = f__integer__($difference(N1, N2)) & f__integer__(N1) = X1 & f__integer__(N2) = X3)) & ?[N3: $int, N4: $int]: ((X5 = f__integer__($difference(N3, N4)) & f__integer__(N3) = X4 & f__integer__(N4) = X2))))))).
tff(statement_6, axiom, ![X: object]: (~(~q_1(X) & ?[N1: $int, N2: $int]: ((N1 = n & $lesseq(1, N2) & $lesseq(N2, N1) & X = f__integer__(N2)))))).
