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

# Returns a list of tuples: preceding char, literal, following char
def process_head(line):
    literals = []
    if line is None:
        return literals
    line = line.strip("\n").strip(".").strip()
    cl = re.search(r'^{(.+):(.+)}$', line)
    if cl:                                                      # { p(X) : q(X),...,t(X) }
        head, body = cl.group(1), cl.group(2).split("%")
        literals.append(("{", head, ":"))
        for i in range(len(body)-1):
            literals.append((None, body[i], None))
        literals.append((None, body[-1], "}"))
        return literals
    choice = re.search(r'^{(.+)}$', line)                       # { p(X) }
    if choice:
        head = choice.group(1)
        literals.append(("{", head, "}"))
        return literals
    for l in line.split("%"):
        literals.append((None, l, None))
    #print("Head literals:", literals)
    return literals

def process_body(line):
    literals = []
    if line is None:
        return literals
    else:
        for l in line.split("%"):
            literals.append((None, l, None))
    return literals

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

# Literals are either positive, negative, or doubly negated (sign)
# An atomic literal has one child (an atom)
# A literal can be preceded by a {, and followed by a } or :
class Literal:
    def __init__(self, name, raw, sign, literal_type, prec_char, foll_char):
        self.name = name
        self.raw = raw
        self.sign = sign
        self.child = None
        self.type = literal_type
        if prec_char is None:
            self.preceding_char = ''
        else:
            self.preceding_char = prec_char
        if foll_char is None:   
            self.following_char = ''
        else:
            self.following_char = foll_char


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
        return line

    def find_literals(self, line_number, line):
        literal_objects = []
        literal_candidates = []
        tup_match = re.findall('\([^\)]+\)', line)                  # Temporarily replace commas within argument lists with @ special character
        replacements = [re.sub(",", "@", m) for m in tup_match]
        for i, m in enumerate(tup_match):
            line = line.replace(m, replacements[i], 1)
        line = line.replace(",", "%")                               # Replace all remaining commas with a special character to denote literals demarkation
        if re.search(r'#', line):
            rule_parts = line.split("#")
            if len(rule_parts) > 1:
                head, body = rule_parts
            else:
                head, body = None, ruleparts[0]
        else:
            head, body = line, None
        head_literals = process_head(head)
        body_literals = process_body(body)
        for l in head_literals:
            literal_candidates.append(l)
        for l in body_literals:
            literal_candidates.append(l)
        lit_counter = 0
        for tup in literal_candidates:
            lit = tup[1].strip("\t").strip()
            print("Literal candidate:", lit)
            if lit:                                                                         # Empty check
                name = "_l" + str(line_number) + "l" + str(lit_counter) + "_"
                if re.search(r'^not not \w', lit):                                          # Doubly negated atom
                    if re.search("<|>|<=|>=|=|!=", lit) is None:                                # Atomic literals
                        lit = re.sub(r'^not not ', "", lit)
                        lit = Literal(name, lit, "double negative", "atomic", tup[0], tup[2])
                    else:                                                                       # Arithmetic literals
                        lit = re.sub(r'^not not ', "", lit)
                        lit = Literal(name, lit, "double negative", "arithmetic", tup[0], tup[2])
                elif re.search(r'^not \w', lit):                                            # Singly negated atom
                    if re.search("<|>|<=|>=|=|!=", lit) is None:                                # Atomic literals
                        lit = re.sub(r'^not ', "", lit)
                        lit = Literal(name, lit, "negative", "atomic", tup[0], tup[2])
                    else:                                                                       # Arithmetic literals
                        lit = re.sub(r'^not ', "", lit)
                        lit = Literal(name, lit, "negative", "arithmetic", tup[0], tup[2])
                else:                                                                       # Positive atom
                    if re.search("<|>|<=|>=|=|!=", lit) is None:                                # Atomic literals
                        lit = Literal(name, lit, "positive", "atomic", tup[0], tup[2])
                    else:                                                                       # Arithmetic literals
                        lit = Literal(name, lit, "positive", "arithmetic", tup[0], tup[2])
                lit_counter += 1
                literal_objects.append(lit)
        self.literals.append(literal_objects)
        print("Literals", self.literals)
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
                        for i in range(4):
                            for t in self.terms:
                                if term == t.name:
                                    term = t.raw
                        arg_list += term + ")"
                    else:
                        arg_list = ""
                    atom = literal.child.pname + arg_list
                    line += literal.preceding_char
                    if literal.sign == "double negative":
                        line += " not not " + atom
                    elif literal.sign == "negative":
                        line += " not " + atom
                    else:
                        line += atom
                    line += literal.following_char
                else:
                    line += literal.preceding_char
                    if literal.sign == "double negative":
                        line += " not not " + literal.raw.strip(".")
                    elif literal.sign == "negative":
                        line += " not " + literal.raw.strip(".")
                    else:
                        line += literal.raw.strip(".")
                    line += literal.following_char
                    for i in range(4):
                        for t in self.terms:
                            if re.search(t.name, line):
                                line = line.replace(t.name, t.raw)
                if literal_counter == 0 and self.rule_types[line_counter] == 1:     # Head :- Body
                    if literal.following_char == ":":                               # Head has form { p(X) : q(X) ... }
                        print("Hello: ", line)
                        pass
                    else:
                        line += " :- "
                elif literal.following_char == "}" and self.rule_types[line_counter] == 1:
                    line += " :- "
                else:
                    if literal.following_char == ":":                               # Head has form { p(X) : q(X) ... }
                        print("Hello: ", line)
                        pass
                    else:
                        line += ","
            for i in range(3):
                for t in self.terms:
                    if re.search(t.name, line):
                        line = line.replace(t.name, t.raw)
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