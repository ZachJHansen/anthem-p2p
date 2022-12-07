import re

def get_preds_prog(filepath):
    predicates = []
    f = open(filepath, "r")
    raw = f.readlines()
    f.close()
    for line in raw:
        line = re.sub(":-", ",", line)                      # Remove rule operators, newlines, and periods
        line = line.strip(".\n")
        line = re.sub(r'\+|\-|\*|\\|\/', "", line)          # Remove arithmetics (e.g. t+1 should be treated as a single term)
        line = re.sub(r'\w+\.\.\w+', "INTERVAL", line)      # Remove intervals
        literals = line.split(",")                          # Split a rule into its literals, remove arithmetic literals (comparisons)
        atomic_literals = [l for l in literals if re.search("<|>|<=|>=|=|!=", l) is None]
        for literal in atomic_literals:
            atom_candidates = re.findall(r'\w+\([^\)]+\)|[a-z]+[a-z\d_]*', literal)
            if len(atom_candidates) > 0:
                atoms = [a for a in atom_candidates if not a == 'not']
                for a in atoms:
                    if "(" in a:                            # First-order atom
                        pname = a.split("(")[0]
                        arity = len(re.findall(",", a)) + 1
                        predicates.append(pname + "/" + str(arity))
                    else:                                   # Propositional atom
                        predicates.append(a + "/0")
    preds = set(predicates)
    print("\nFound the following predicates in file: " + filepath + ":")
    print("\t", preds)
    return preds


preds = get_preds_prog("new-primes_int.3.lp")
