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
tff(type, type, go: (object * object) > $o).
tff(type, type, go_1: (object * object) > $o).
tff(type, type, goto: (object * object * object) > $o).
tff(type, type, in: (object * object * object) > $o).
tff(type, type, in0: (object * object) > $o).
tff(type, type, in_building: (object * object) > $o).
tff(type, type, in_building_1: (object * object) > $o).
tff(type, type, person: (object) > $o).
% function types
tff(type, type, h: $int).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% assumptions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tff(statement_1, axiom, $greatereq(h, 0)).
tff(statement_2, axiom, ![X1: object, X2: object]: ((in0(X1, X2) => person(X1)))).
tff(statement_3, axiom, ![X1: object, X2: object, X3: object]: ((goto(X1, X2, X3) => person(X1)))).
tff(statement_4, axiom, ![X1: object, X2: object, X3: object]: ((in(X1, X2, X3) => person(X1)))).
tff(statement_5, axiom, ![X1: object, X2: object]: (in_building_1(X1, X2) <=> ?[X3: object]: (in(X1, X3, X2)))).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% lemmas
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tff(statement_1, axiom, ![X1: object, X2: object, X3: object]: ((in(X1, X2, X3) => ((in0(X1, X2) & X3 = f__integer__(0)) | ?[X4: object]: ((goto(X1, X2, X4) & ?[N1: $int]: ((X3 = f__integer__($sum(N1, 1)) & f__integer__(N1) = X4)))) | ?[X5: object]: ((in(X1, X2, X5) & ~go_1(X1, X5) & ?[N2: $int, N3: $int]: ((?[N4: $int]: ((N2 = $difference(N4, 1) & N4 = h)) & $lesseq(0, N3) & $lesseq(N3, N2) & X5 = f__integer__(N3))) & ?[N5: $int]: ((X3 = f__integer__($sum(N5, 1)) & f__integer__(N5) = X5)))))))).
tff(statement_2, axiom, ![X1: object, X2: object, X3: object]: ((((in0(X1, X2) & X3 = f__integer__(0)) | ?[X4: object]: ((goto(X1, X2, X4) & ?[N1: $int]: ((X3 = f__integer__($sum(N1, 1)) & f__integer__(N1) = X4)))) | ?[X5: object]: ((in(X1, X2, X5) & ~go_1(X1, X5) & ?[N2: $int, N3: $int]: ((?[N4: $int]: ((N2 = $difference(N4, 1) & N4 = h)) & $lesseq(0, N3) & $lesseq(N3, N2) & X5 = f__integer__(N3))) & ?[N5: $int]: ((X3 = f__integer__($sum(N5, 1)) & f__integer__(N5) = X5))))) => in(X1, X2, X3)))).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% completed definitions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% completed definition of go/2
tff(completed_definition_go_2, axiom, ![X1: object, X2: object]: (go(X1, X2) <=> ?[X3: object]: (goto(X1, X3, X2)))).
% completed definition of go_1/2
tff(completed_definition_go_1_2, axiom, ![X1: object, X2: object]: (~go_1(X1, X2))).
% completed definition of in/3
tff(completed_definition_in_3, axiom, ![X1: object, X2: object, X3: object]: (in(X1, X2, X3) <=> ((in0(X1, X2) & X3 = f__integer__(0)) | ?[X4: object]: ((goto(X1, X2, X4) & ?[N1: $int]: ((X3 = f__integer__($sum(N1, 1)) & f__integer__(N1) = X4)))) | ?[X5: object]: ((in(X1, X2, X5) & ~go(X1, X5) & ?[N2: $int]: (($lesseq(0, N2) & $lesseq(N2, $difference(h, 1)) & X5 = f__integer__(N2))) & ?[N3: $int]: ((X3 = f__integer__($sum(N3, 1)) & f__integer__(N3) = X5))))))).
% completed definition of in_building/2
tff(completed_definition_in_building_2, axiom, ![X1: object, X2: object]: (in_building(X1, X2) <=> ?[X3: object]: (in(X1, X3, X2)))).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% integrity constraints
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tff(integrity_constraint, axiom, ![X1: object, X2: object, X3: object, X4: object]: (~(in(X1, X2, X3) & in(X1, X4, X3) & X2 != X4))).
tff(integrity_constraint, axiom, ![X1: object, X2: object]: (~(~in_building(X1, X2) & person(X1) & ?[N: $int]: (($lesseq(0, N) & $lesseq(N, h) & X2 = f__integer__(N)))))).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% specs
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tff(statement_1, axiom, ![X1: object, X2: object, X3: object]: (in(X1, X2, X3) <=> ((in0(X1, X2) & X3 = f__integer__(0)) | ?[X4: object]: ((goto(X1, X2, X4) & ?[N1: $int]: ((X3 = f__integer__($sum(N1, 1)) & f__integer__(N1) = X4)))) | ?[X5: object]: ((in(X1, X2, X5) & ?[N2: $int, N3: $int]: ((?[N4: $int]: ((N2 = $difference(N4, 1) & N4 = h)) & $lesseq(0, N3) & $lesseq(N3, N2) & X5 = f__integer__(N3))) & in(X1, X2, X3) & ?[N5: $int]: ((X3 = f__integer__($sum(N5, 1)) & f__integer__(N5) = X5))))))).
tff(statement_2, conjecture, ![X1: object, X2: object, X3: object, X4: object]: (~(in(X1, X2, X3) & in(X1, X4, X3) & X2 != X4))).
