# ANTHEM-P2P
# Zach Hansen
# 12/07/22
#
# This script automates the process of confirming the equivalence of 
# two ASP programs using ANTHEM.
# 
# Given an original file (the first user-provided .lp), an alternative file (the second .lp), and a context file (the .ug file), ANTHEM-P2P:
# 1. Computes the completion of original.lp and prints to file original.txt
#   a. Private predicates (p) are renamed (p_1) to avoid conflicts with private predicates in alternative.lp
# 2. Produces a new specification file by combining context.ug and original.txt (completion.spec)
#   a. Completed definitions of public predicates from original.lp are treated as specs
#   b. Completed definitions of private predicates from original.lp are treated as assumptions
#   c. Every private predicate is added as an input predicate to the final spec
# 3. Verifies that alternative.lp implements completion.spec
#   a. All private predicates (q) in alternative.lp are renamed (q_2)
#
# Additional Information:
# 1. Running ANTHEM-P2P once constitutes a proof in BOTH directions:
#   a. Vampire verifies the formula UG + COMP[P1] <-> COMP[P2]
# 2. If a predicate symbol occurs in context.ug, it is a public predicate
#   a. All other predicate symbols (from either program) are private predicates
# 3. If you wish to provide lemmas or axioms to assist Vampire, their file names should be listed after the main 3 arguments
#   a. If you wish to provide these auxiliary files, a .ug must be provided as well
# 4. Some CLINGO constructs are not supported by ANTHEM-P2P
#   a. Any programs provided as arguments will have their #show statements removed
#   b. Eventually, variable names will be overwritten automatically to X,Y,Z (I,J,K) variants
#
# ACTIVE BUGS
#   1. Comments
#   2. Regex confuses q/1 with q/2 (need to incorporate arity in predicate renaming replacements)
#
# FEATURES TO CHECK
#   1. Processing integrity constraints in orig.lp
#   2. Substring confusion - more_than_three, three
#   3. Processing programs with #show statements
#   4. Use input statements from the UG instead of an empty spec when generating completions
#   5. Variable names must start with X,Y,Z (I,J,K)

import sys, re
import subprocess as sproc

def parse_lemmas(args):
    aux = []
    spec_exp = r'.*.spec'
    for fname in args:
        if re.search(spec_exp, fname):
            f = open(fname, "r")
            lines = f.readlines()
            f.close()
            for l in lines:
                aux.append(l)
        else:
            print("Failed to parse file ", fname, " - expected a .spec file. Stopping.")
            sys.exit(1)
    return aux

def parse_cmd():
    files = {}
    lp_exp = r'.*.lp$'
    ug_exp = r'.*.ug$'
    f1 = sys.argv[1].strip()
    f2 = sys.argv[2].strip()
    f3 = sys.argv[3].strip()
    # Find first .lp, second .lp, only .ug
    if re.search(lp_exp, f1):
        files["orig"] = f1
        if re.search(lp_exp, f2):
            files["alt"] = f2
            files["ctx"] = f3
        else:
            files["alt"] = f3
            files["ctx"] = f2
    else:
        files["orig"] = f2
        files["alt"] = f3
        files["ctx"] = f1
    # Add the contents of any remaining files as a list of lemmas and axioms
    aux = None
    if len(sys.argv) > 4:
        aux = parse_lemmas(sys.argv[4:])
    # Sanity Check
    if not re.search(lp_exp, files["orig"]):
        print("Error (1) parsing program arguments: expects 2 files with .lp extension, and 1 file with a .ug extension")
        sys.exit(1)
    if not re.search(lp_exp, files["alt"]):
        print("Error (2) parsing program arguments: expects 2 files with .lp extension, and 1 file with a .ug extension")
        sys.exit(1)
    if not re.search(ug_exp, files["ctx"]):
        print("Error (3) parsing program arguments: expects 2 files with .lp extension, and 1 file with a .ug extension")
        sys.exit(1)
    print("\n####### Input Files (Original, Alternative, Context) #######")
    print(files)
    print("")
    return files, aux

# Process the Anthem output and save the completed definitions to a text file
def store_completion(completions, file_path):
    with open(file_path, "w") as f:
        for c in completions:
            f.write(c)
            if c[-1] != "\n":
                f.write("\n")
    sproc.run("chmod 666 " + file_path, shell=True)

# Run Anthem (forward direction) on the lp at file_path against a specification containing the input statements
def generate_completion(file_path, inputs):
    # Create a temporary specification file
    name = file_path.split("/")[-1].strip()
    name = name.replace(".lp", "-completion.spec")
    empty_spec = "temp-" + name
    spec_gen_output = sproc.run("touch " + empty_spec, shell=True)
    if inputs is not None:
        with open(empty_spec, "w") as f:
            for pred in inputs:
                f.write("input: " + pred + ".\n")
        f.close()
    # Run Anthem
    try:
        anthem_output = sproc.run("./anthem verify-program --proof-direction=forward " + file_path + " " + empty_spec, encoding='utf-8', stdout=sproc.PIPE, shell=True)
        anthem_output.check_returncode()
    except sproc.CalledProcessError:
        print("Error running anthem: ", anthem_output.stderr)
        sys.exit(1)
    # Store the completed definitions in a text file for easy reading
    name = name.replace(".spec", ".txt")
    exp = r'completed definition of.+\n|integrity constraint:.+'
    completions = re.findall(exp, anthem_output.stdout)
    store_completion(completions, name)
    sproc.call("rm " + empty_spec, shell=True)
    # Pass completed definitions back to main
    return completions

# Returns: a mapping from original predicate names to their new names
def renamed(preds, addendum=1):
    renames = []
    for pn in preds:
        p = pn.split("/")[0]
        n = pn.split("/")[1]
        new_p = p + "_" + str(addendum) + "/" + n
        renames.append(new_p)
    mapping = dict(zip(preds, renames))
    if addendum == 1:
        print("\nRenaming predicates from the original program...")
    else:
        print("\nRenaming predicates from the alt program...")
    print("\t", mapping)
    return mapping

# Find all predicate symbols p/n occurring in the list of strings
def get_preds_prog(raw, fp):
    predicates = []
    for line in raw:
        line = re.sub(":-", ",", line)                      # Remove rule operators, newlines, and periods
        line = line.strip(".\n")
        line = re.sub(r'\+|\-|\*|\\|\/', "", line)          # Remove arithmetics (e.g. t+1 should be treated as a single term)
        line = re.sub(r'\w+\.\.\w+', "INTERVAL", line)      # Remove intervals
        tup_match = re.findall('\([^\)]+\)', line)          # Replace commas within argument lists with @ special character
        replacements = [re.sub(",", "@", m) for m in tup_match]
        for i, m in enumerate(tup_match):
            line = line.replace(m, replacements[i], 1)
        literals = line.split(",")                          # Split a rule into its literals, remove arithmetic literals (comparisons)
        atomic_literals = [l for l in literals if re.search("<|>|<=|>=|=|!=", l) is None]
        for literal in atomic_literals:
            atom_candidates = re.findall(r'\w+\([^\)]+\)|[a-z]+[a-z\d_]*', literal)
            if len(atom_candidates) > 0:
                atoms = [a for a in atom_candidates if not a == 'not']
                for a in atoms:
                    if "(" in a:                            # First-order atom
                        pname = a.split("(")[0]
                        arity = len(re.findall("@", a)) + 1
                        predicates.append(pname + "/" + str(arity))
                    else:                                   # Propositional atom
                        predicates.append(a + "/0")
    preds = set(predicates)
    print("\nFound the following predicates in file: " + fp + ":")
    print("\t", preds)
    return preds

# Given a mapping from predicate names to new names, a predicate symbol, and a text string
# Replace all occurrences of the predicate symbol with its new name in the text string and return it
def replace_predicate(mapping, pred, spec):
    pname = pred.split("/")[0]                                      # Extract p from p/n
    arity = int(pred.split("/")[1])                                 # Extract n from p/n
    new_name = mapping[pred].split("/")[0]                          # Extract p_1 from p_1/n
    if arity > 0:
        start = '^' + pname + '\([^\)]+'
        non_word_start = '\W' + pname + '\([^\)]+'
        for _ in range(arity-1):
            start += ',[^\)]+'
            non_word_start += ',[^\)]+'
        start += '\)'
        non_word_start += '\)'
        pattern = start + '|' + non_word_start
        base_exp = re.compile(pattern)                              # Match pname(...)
    else:
        pattern = r'\W' + pname + r'\W|^' + pname + r'\W'           # Match pname
        base_exp = re.compile(pattern) 
    occs = re.findall(base_exp, spec)                               # Find matching substrings
    renamed = [re.sub(pname, new_name, o) for o in occs]            # Replace the predicate name within each matched substring
    replace_map = dict(zip(occs, renamed))
    for key in replace_map.keys():
        print("\tReplacing expression", key, "with expression", replace_map[key])
    print("")

    matchbox = [m for m in base_exp.finditer(spec)]
    if len(matchbox) > 0:
        new_spec = spec[0:matchbox[0].span()[0]]                        # Add the string up to the first match
        for i, m in enumerate(matchbox):
            new_spec += renamed[i]                                      # Add the match with the new name subbed in
            if i+1 < len(matchbox):
                nxt = matchbox[i+1]
                new_spec += spec[m.span()[1]:nxt.span()[0]]             # Add the string up to the next match
        last = matchbox[-1].span()[1]
        if last < len(spec):                                            # Add any remaining string after the matches
            new_spec += spec[last: len(spec)]
    else:                                                               # If no matches, return the original line
        new_spec = spec
    return new_spec


def terminator(spec):
    if spec[-1] == "\n":
        if spec[-2] != ".":
            spec = spec.replace("\n", ".\n")
            return spec
        else:
            return spec
    elif spec[-1] == ".":
        spec = spec + "\n"
        return spec
    else:
        spec = spec + ".\n"
        return spec

# Input: A list of completed definitions from original.lp
# Input: The file path pointing to the user guide
# Input: A list of private predicates occurring in original.lp
# Input: A list of public predicates occurring in original.lp
# Input: A string of helper lemmas
# Output: The file path pointing to the resulting spec
def generate_spec(completions, context_path, privates, publics, aux):
    # Final spec should combine the completed definitions from the text file at completion_path with the context at context_path
    # Don't change the original context, just create a new, extended version
    final_spec = re.sub(".ug", "-final.spec", context_path)
    spec_gen_output = sproc.run("cp " + context_path + " " + final_spec, shell=True)
    sproc.run("chmod oug+rw " + final_spec, shell=True)

    # First add all lemmas and axioms from aux
    spec_string = "\n"
    if aux is not None:
        for line in aux:
            spec_string += "\n" + line

    # Second add all completions as either assumptions or specs, and all integrity constraints as specs
    # First occurence of forall OR a word followed by iff starts completed definition
    # First occurence of forall OR a not starts an integrity constraint
    comp_exp = r'definition of +(.+): *(forall.*$)|definition of +(.+): *(\w ?<->.+$)'
    cons_exp = r'constraint.+(forall.*$)|constraint.+.*: ?(not.+$)'
    for line in completions:
        comp = re.search(comp_exp, line)
        cons = re.search(cons_exp, line)
        if comp:
            predicate = comp.group(1)
            if predicate in privates:
                spec = "assume: " + comp.group(2)
                spec_string += terminator(spec)
                inp = "input: " + predicate
                spec_string += terminator(inp)
            elif predicate in publics:
                spec = "spec: " + comp.group(2)
                spec_string += terminator(spec)
            else:
                print("Unknown predicate: ", predicate)
        elif cons:
            spec = "spec: " + cons.group(1)
            spec_string += terminator(spec)
        else:
            print("Parsing error: couldn't find a completed definition or an integrity constraint in:")
            print(line)
            sys.exit(1)

    with open(final_spec, "a") as f2:
        f2.write(spec_string)
    f2.close()
    return final_spec

# Verify lp against spec
def verify(lp_path, spec_path):
    try:
        anthem_output = sproc.run("./anthem verify-program " + lp_path + " " + spec_path, encoding='utf-8', stdout=sproc.PIPE, shell=True)
        anthem_output.check_returncode()
    except sproc.CalledProcessError:
        print("Error running anthem: ", anthem_output.stderr)
        sys.exit(1)
    print(anthem_output.stdout)

# Removes #show statements and comments from input programs
# Renames private predicates from fp (any predicate not occurring in publics)
# Returns a mapping from every private predicate to its renamed version
# Returns a list of public predicates occurring in fp
def preprocess(fp, ug_publics, file_type):
    outp = []                                                           # Assemble list of anthem-compliant lines
    comm_exp = r'%.*$'
    show_exp = r'^#show.*$'
    var_exp = r'\b[A-Z]{1}[\w\']*\b'
    with open(fp, "r") as f:
        raw = f.readlines()
        for line in raw:
            if re.search(show_exp, line) is None:
                line = re.sub(comm_exp, '', line)
                if line and not re.search(r'^\s*$', line):
                    outp.append(line)
    f.close()
    lp_publics = []                                                     # Rename private predicates
    lp_privates = []
    all_preds = get_preds_prog(outp, fp)
    for pred in all_preds:
        if pred in ug_publics:
            lp_publics.append(pred)
        else:
            lp_privates.append(pred)
    mapping = renamed(lp_privates, file_type)
    for i, line in enumerate(outp):
        for pred in lp_privates:
            line = replace_predicate(mapping, pred, line)
        outp[i] = line
    newfp = "new-"+fp                                                   # Write to new file
    with open(newfp, "w") as f:
        f.writelines(outp)
    f.close()
    return lp_privates, lp_publics

# All predicates occurring in an "input: p/n" or "output: p/n" statement
# are considered public predicates. Input publics are used to 
# construct an initial specification during completion generation
def get_ug_preds(fp):
    inputs = []
    outputs = []
    inp_exp = r'^input:.+$'
    outp_exp = r'^output:.+$'
    pred_exp = r'\w+/\d+.|\w+/\d+ *,'
    if fp is not None:
        with open(fp, "r") as f:
            raw = f.readlines()
            for line in raw:
                if re.search(inp_exp, line) is not None:
                    line = re.sub(r'^input:', "", line)
                    predicates = re.findall(pred_exp, line)
                    for p in predicates:
                        inputs.append(re.sub(r'[., ]', "", p))
                elif re.search(outp_exp, line) is not None:
                    line = re.sub(r'^output:', "", line)
                    predicates = re.findall(pred_exp, line)
                    for p in predicates:
                        outputs.append(re.sub(r'[., ]', "", p))
                else:
                    pass
        f.close()
        print("####### Input predicates from UG: #######")
        print(inputs)
        print("\n####### Output predicates from UG: #######")
        print(outputs)
        return inputs, outputs
    else:
        print("Fatal error")
        sys.exit(1)

if __name__ == "__main__":
    assert (sys.version_info >= (3, 6, 9)), "This script requires Python v3.6.9 (or later). Try python3"
    files, aux = parse_cmd()
    inputs, outputs = get_ug_preds(files["ctx"])
    public_preds = list(set(inputs + outputs))
    orig_privates, orig_publics = preprocess(files["orig"], public_preds, 1)
    alt_privates, alt_publics = preprocess(files["alt"], public_preds, 2)
    files["orig"] = "new-"+files["orig"]
    files["alt"] = "new-"+files["alt"]
    completions = generate_completion(files["orig"], inputs)
    if files["ctx"]:
        final_spec = generate_spec(completions, files["ctx"], orig_publics, orig_privates, aux) 
    else:
        sproc.call("touch .spec", shell=True)
        final_spec = generate_spec(completions, ".spec", orig_publics, orig_privates, aux) 
    verify(files["alt"], final_spec)
