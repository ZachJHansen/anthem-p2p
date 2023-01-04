# Classes for constructing a simplified AST for Anthem-P2P

import re, sys

# 1 = Head :- Body, 2 = :- Body, 3 = Head, 4 = B,..,B.
def find_rtype(line, previous_line):
    if previous_line is not None:
        pl = previous_line.strip()
        if re.search(r',\s*\n*$', pl):
            return 4
    if re.search(r'#', line) is None:
        return 3
    else:
        head, body = line.split("#")
        if head and head.strip():
            return 1
        else:
            return 2

def terminator(spec, next_rtype):
    if spec[-1] == "\n":
        if spec[-2] == ",":
            if next_rtype == 4:
                return spec
            else:
                return spec[:-2] + "."
        elif spec[-2] != ".":
            spec = spec.replace("\n", ".\n")
            return spec
        else:
            return spec
    elif spec[-1] == ",":
        if next_rtype == 4:
            return spec + "\n"
        else:
            return spec[:-1] + ".\n"
    elif spec[-1] == ".":
        spec = spec + "\n"
        return spec
    else:
        spec = spec + ".\n"
        return spec

# Intervals, integers, symbolic constants, and integers are leaf terms
# Unary operations are terms with one child, binary operations have two
class Term:
    def __init__(self, name, raw, children=None, operator=None):
        self.name = name
        self.raw = raw
        self.children = children
        self.operator = operator

# Atoms consist of a predicate symbol and a list of terms (arguments)
class Atom:
    def __init__(self, raw):
        self.predicate = None
        self.pname = None
        self.arity = None
        self.arguments = None
        match = re.search(r'\w+\([^\)]+\)|[a-z]+[a-z\d_]*', raw)
        if match:
            atom = match.group()
            if "(" in atom:                             # First-order atom
                self.pname, arg_string = atom.split("(")
                self.arguments = arg_string.strip(")").split("@")
                self.arity = len(self.arguments)
            else:                                       # Propositional atom
                self.pname = atom
                self.arity = 0
            self.predicate = self.pname + "/" + str(self.arity)
        else:
            print("Fatal error.")
            sys.exit(1)

# Literals are either positive or default negated (sign)
# An atomic literal has one child (an atom)
class Literal:
    def __init__(self, name, raw, sign, literal_type):
        self.name = name
        self.raw = raw
        self.sign = sign
        self.child = None
        self.type = literal_type


# A program is a list of lines
# A line is a list of literals
class Program:
    def __init__(self, name, raw, verbose=False):
        self.name = name
        self.raw = raw
        self.terms = []
        self.predicates = set()
        self.privates = set()
        self.inputs = set()
        self.outputs = set()
        self.literals = []
        self.compliant_lines = []
        self.rule_types = []            
        self.v = verbose
        if verbose:
            print("\n###### Preprocessing program ######")
        program_lines = [re.sub(r'%.*$', '', line) for line in raw if re.search(r'^#show.*$', line) is None]
        for counter, line in enumerate(program_lines):
            line = line.strip("\n")
            line = self.find_terms(counter, line)
            line = self.find_literals(counter, line)
            if counter == 0:
                rtype = find_rtype(line, None)
            else:
                rtype = find_rtype(line, program_lines[counter-1])
            self.compliant_lines.append(line)
            self.rule_types.append(rtype)
        if verbose:
            print("Compliant lines:", self.compliant_lines)
        for literal_list in self.literals:
            if verbose:
                print("\tLiterals:")
            for literal in literal_list:
                if verbose:
                    print("\t\tLiteral:", literal.raw)
                if literal.type == "atomic":
                    atom = Atom(literal.raw)
                    if verbose:
                        print("\t\t\tAtom:", atom.predicate)
                    self.predicates.add(atom.predicate)
                    literal.child = atom

    def rename_predicates(self, inputs, outputs, addendum):
        for predicate in self.predicates:
            if predicate in inputs:
                self.inputs.add(predicate)
            elif predicate in outputs:
                self.outputs.add(predicate)
            else:
                self.privates.add(predicate)
        for line_index, literal_list in enumerate(self.literals):
            comp_line = self.compliant_lines[line_index]
            for literal in literal_list:
                if literal.type == "atomic":  
                    if literal.child.predicate in self.privates:
                        literal.child.pname = literal.child.pname + "_" + str(addendum)
                        literal.child.predicate = literal.child.pname + "/" + str(literal.child.arity)
        
    # Input: A string representing a line of the program and the line number
    # Action: Constructs a mapping from terms encountered in the line to their abstract representations
    # Output: The line with terms replaced with abstractions
    def find_terms(self, line_number, line):
        term_counter = 0
        line = re.sub(r':-', "#", line)       

        aim1 = [re.sub(r'[\+\-\*\\\/] *', "", match).strip() for match in re.findall(r'[\+\-\*\\\/] *\([^\)]+\)', line)]
        aim2 = [re.sub(r'[\+\-\*\\\/] *', "", match).strip() for match in re.findall(r'\([^\)]+\) *[\+\-\*\\\/]', line)]
        arithmetic_interval_matches = aim1 + aim2
        for match in arithmetic_interval_matches:
            term_counter += 1
            term = Term("_l" + str(line_number) + "t" + str(term_counter) + "_", match)
            self.terms.append(term)
            line = line.replace(term.raw, term.name)

        interval_matches = re.findall(r'\w+\.\.\w+', line)
        for match in interval_matches:
            term_counter += 1
            term = Term("_l" + str(line_number) + "t" + str(term_counter) + "_", match)
            self.terms.append(term)
            line = line.replace(term.raw, term.name)

        bin_op_matches = re.findall(r'\w+ *[\+\-\*\\\/] *\w+', line)
        for match in bin_op_matches:
            term_counter += 1
            name = "_l" + str(line_number) + "t" + str(term_counter) + "_"
            decompose = re.search(r'(\w+ *)([\+\-\*\\\/])( *\w+)', match)
            term = Term(name, match, [decompose.group(1), decompose.group(3)], decompose.group(2))
            self.terms.append(term)
            line = line.replace(term.raw, term.name)

        unary_op_matches = re.findall(r'-\w+', line) 
        for match in unary_op_matches:
            term_counter += 1
            name = "_l" + str(line_number) + "t" + str(term_counter) + "_"
            decompose = re.search(r'(-)(\w+)', match)
            term = Term(name, match, [decompose.group(1)], decompose.group(2))
            self.terms.append(term)
            line = line.replace(term.raw, term.name)
        return line

    def find_literals(self, line_number, line):
        literal_objects = []
        tup_match = re.findall('\([^\)]+\)', line)                  # Temporarily replace commas within argument lists with @ special character
        replacements = [re.sub(",", "@", m) for m in tup_match]
        for i, m in enumerate(tup_match):
            line = line.replace(m, replacements[i], 1)
        line = line.replace(",", "%")                               # Replace all remaining commas with a special character to denote literals demarkation
        literals = re.split(r'%|#', line)
        atomic_literals = [l.strip("\t") for l in literals if re.search("<|>|<=|>=|=|!=", l) is None]
        arithmetic_literals = [l.strip("\t") for l in literals if re.search("<|>|<=|>=|=|!=", l) is not None]
        lit_counter = 0
        for lit in atomic_literals:
            if lit and lit.strip():
                name = "_l" + str(line_number) + "l" + str(lit_counter) + "_"
                if re.search(r'\Wnot\W', lit):
                    lit = re.sub(r'\Wnot\W', "", lit)
                    lit = Literal(name, lit, "negative", "atomic")
                else:
                    lit = Literal(name, lit, "positive", "atomic")
                literal_objects.append(lit)
            else:
                pass
            lit_counter += 1
        for lit in arithmetic_literals:
            if lit and lit.strip():
                name = "_l" + str(line_number) + "l" + str(lit_counter) + "_"
                if re.search(r'\Wnot\W', lit):
                    lit = re.sub(r'\Wnot\W', "", lit)
                    lit = Literal(name, lit, "negative", "arithmetic")
                else:
                    lit = Literal(name, lit, "positive", "arithmetic")
                literal_objects.append(lit)
            else:
                pass
        self.literals.append(literal_objects)
        return line

    def print_program(self, fp):
        lines = []
        for line_counter, literal_list in enumerate(self.literals):
            line = ''
            for literal_counter, literal in enumerate(literal_list):
                if literal_counter == 0 and self.rule_types[line_counter] == 2:                  # Constraint
                    line += ":- "
                if literal.type == "atomic":
                    if literal.child.arguments is not None:
                        arg_list = "("
                        for i in range(len(literal.child.arguments)-1):
                            term = literal.child.arguments[i]
                            for i in range(3):                                          # Term replacement goes 3 levels deep?
                                for t in self.terms:
                                    if term == t.name:
                                        term = t.raw
                            arg_list += term + ","
                        term = literal.child.arguments[-1]
                        for i in range(3):
                            for t in self.terms:
                                if term == t.name:
                                    term = t.raw
                        arg_list += term + ")"
                    else:
                        arg_list = ""
                    atom = literal.child.pname + arg_list
                    if literal.sign == "negative":
                        line += " not " + atom
                    else:
                        line += atom
                else:
                    if literal.sign == "negative":
                        line += " not " + literal.raw.strip(".")
                    else:
                        line += literal.raw.strip(".")
                    for t in self.terms:
                        if re.search(t.name, line):
                            line = line.replace(t.name, t.raw)

                if literal_counter == 0 and self.rule_types[line_counter] == 1:     # Head :- Body
                    line += " :- "
                else:
                    line += ","
            if line and line.strip():
                if line_counter == len(self.literals)-1:
                    line = terminator(line, 1)
                else:
                    line = terminator(line, self.rule_types[line_counter+1])
            lines.append(line)
        if self.v:
            print("Lines:", lines)
        with open(fp, "w") as f:
            f.writelines(lines)
        f.close()
                

