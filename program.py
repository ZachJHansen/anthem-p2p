# Classes for constructing a simplified AST for Anthem-P2P

import re, sys

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
    def __init__(self, name, raw):
        self.name = name
        self.raw = raw
        self.terms = []
        self.predicates = set()
        self.privates = set()
        self.publics = set()
        self.literals = []
        self.compliant_lines = []
        self.renamed_lines = []
        program_lines = [re.sub(r'%.*$', '', line) for line in raw if re.search(r'^#show.*$', line) is None]
        for counter, line in enumerate(program_lines):
            line = line.strip("\n")
            line = self.find_terms(counter, line)
            line = self.find_literals(counter, line)
            self.compliant_lines.append(line)
        for literal_list in self.literals:
            for literal in literal_list:
                if literal.type == "atomic":
                    atom = Atom(literal.raw)
                    self.predicates.add(atom.predicate)
                    literal.child = atom

    def rename_predicates(self, publics, addendum):
        for predicate in self.predicates:
            if predicate in publics:
                self.publics.add(predicate)
            else:
                self.privates.add(predicate)
        for line_index, literal_list in enumerate(self.literals):
            comp_line = self.compliant_lines[line_index]
            for literal in literal_list:
                if literal.type == "atomic":  
                    if literal.child.arguments is not None:          
                        arg_list = "("
                        for i in range(len(literal.child.arguments)-1):
                            arg_list += literal.child.arguments[i] + "@"
                        arg_list += literal.child.arguments[-1] + ")"
                    else:
                        arg_list = ""
                    old_atom = literal.child.pname + arg_list
                    if literal.child.predicate in self.privates:
                        literal.child.pname = literal.child.pname + "_" + str(addendum)
                        literal.child.predicate = literal.child.pname + "/" + str(literal.child.arity)
                    new_atom = literal.child.pname + arg_list
                    comp_line = comp_line.replace(old_atom, new_atom)
            self.renamed_lines.append(comp_line)
        
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
        atomic_literals = [l for l in literals if re.search("<|>|<=|>=|=|!=", l) is None]
        arithmetic_literals = [l for l in literals if re.search("<|>|<=|>=|=|!=", l) is not None]
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
        for i, line in enumerate(self.renamed_lines):
            if line and line.strip():
                line = line.replace("#", ":-")
                line = re.sub(r'%|@', ",", line)
                term_pattern = re.compile("_l" + str(i) + "t\d+_")
                match = re.search(term_pattern, line)
                while match:
                    term = [t for t in self.terms if t.name == match.group()][0]
                    line = line.replace(term.name, term.raw)
                    match = re.search(term_pattern, line)
                lines.append(line + "\n")
        with open(fp, "w") as f:
            f.writelines(lines)
        f.close()
                

