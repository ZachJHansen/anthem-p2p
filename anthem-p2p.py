# ANTHEM-P2P
# Zach Hansen
# 11/21/22
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
#   1. Variable names must start with X,Y,Z (I,J,K)
#
# FEATURES TO CHECK
#   1. Processing integrity constraints in orig.lp
#   2. Substring confusion - more_than_three, three
#   3. Processing programs with #show statements
#   4. Use input statements from the UG instead of an empty spec when generating completions

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
    return name, completions

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

# Find all predicate symbols p/n occurring in the program at filepath
def get_preds_prog(filepath):
    predicates = []
    f = open(filepath, "r")
    raw = f.readlines()
    f.close()
    for line in raw:
        #print("Processing line", line)
        line = re.sub(":-", ",", line)                      # Remove rule operators, newlines, and periods
        line = line.strip(".\n")
        line = re.sub(r'\+|\-|\*|\\|\/', "", line)                 # Remove arithmetics (e.g. t+1 should be treated as a single term)
        line = re.sub(r'\w+\.\.\w+', "INTERVAL", line)      # Remove intervals
        #print("Post-processing line", line)
        atom_candidates = re.findall(r'\w+\([^\)]+\)|[a-z]+[a-z\d_]*', line)
        #print("Atom candidates: ", atom_candidates)
        if len(atom_candidates) > 0:
            atoms = [a for a in atom_candidates if not a == 'not']
            for a in atoms:
                if "(" in a:                                # First-order atom
                    pname = a.split("(")[0]
                    arity = len(re.findall(",", a)) + 1
                    predicates.append(pname + "/" + str(arity))
                else:                                       # Propositional atom
                    predicates.append(a + "/0")
    preds = set(predicates)
    print("\nFound the following predicates in file: " + filepath + ":")
    print("\t", preds)
    return preds

# Returns: a list of predicate symbols from original.lp that are private
# Returns: a list of predicate symbols from original.lp that are public
def get_predicate_list(comp_raw, context):
    ctx_file = open(context, "r")
    ctx_raw = ctx_file.readlines()
    ctx_file.close()
    inputs = []
    outputs = []
    for line in ctx_raw:
        if re.search(r'input:', line):
            p_list = re.sub(r'input:', "", line).strip("\n")
            for p in p_list.split(","):
                # Distinguish between predicates (name/arity) and other types of input (e.g. n->integer)
                if re.search(r'\w/\d', p):                              
                    inputs.append(p.strip(".").strip())
        if re.search(r'output:', line):
            p_list = re.sub(r'output:', "", line).strip("\n")
            for p in p_list.split(","):
                outputs.append(p.strip(".").strip())
    publics = inputs + outputs
    privates = []
    for line in comp_raw:
        if line:
            predicate = re.search(r'of .*:', line)
            if predicate:
                pred = re.sub("of ", "", predicate.group().strip(":"))
                if pred not in publics:
                    privates.append(pred)
    return renamed(privates), publics

# Given a mapping from predicate names to new names, a predicate symbol, and a text string
# Replace all occurrences of the predicate symbol with its new name in the text string and return it
def replace_predicate(mapping, pred, spec):
    pname = pred.split("/")[0]                                      # Extract p from p/n
    arity = pred.split("/")[1]                                      # Extract n from p/n
    new_name = mapping[pred].split("/")[0]                          # Extract p_1 from p_1/n
    if int(arity) > 0:
        #base_exp = r'[^\w]?' + pname + r'\('                        # Match 0 or 1 non-word char followed by pname(
        base_exp = r'\W' + pname + r'\(|^' + pname + r'\('           # Match non-word strings followed by pname(, or pname(
    else:
        #base_exp = r'[^\w]?' + pname + r'[^\w]'                     # Match 0 or 1 non-word char followed by pname
        #base_exp = r'\W' + pname + r'\(|' + pname + r'\('           # Match non-word strings followed by pname(, or pname(
        base_exp = r'\W' + pname + r'\W|^' + pname + r'\W'                     # Match 1 non-word char or string start followed by pname
    base_exp = re.compile(base_exp)
    occs = re.findall(base_exp, spec)                               # Find matching substrings
    renamed = [re.sub(pname, new_name, o) for o in occs]            # Replace the predicate name within each matched substring
    replace_map = dict(zip(occs, renamed))
    for key in replace_map.keys():
        print("\tReplacing expression", key, "with expression", replace_map[key])
    print("")

    matchbox = [m for m in base_exp.finditer(spec)]
    new_spec = spec[0:matchbox[0].span()[0]]                        # Add the string up to the first match
    for i, m in enumerate(matchbox):
        new_spec += renamed[i]                                      # Add the match with the new name subbed in
        if i+1 < len(matchbox):
            nxt = matchbox[i+1]
            new_spec += spec[m.span()[1]:nxt.span()[0]]             # Add the string up to the next match
    last = matchbox[-1].span()[1]
    if last < len(spec):                                            # Add any remaining string after the matches
        new_spec += spec[last: len(spec)]
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

def generate_spec(completions, context_path, aux):
    privates_map, publics = get_predicate_list(completions, context_path)
    # Final spec should combine the completed definitions from the text file at completion_path with the context at context_path
    final_spec = re.sub(".ug", "-final.spec", context_path)
    # Don't change the original context, just create a new, extended version
    spec_gen_output = sproc.run("cp " + context_path + " " + final_spec, shell=True)
    sproc.run("chmod 666 " + final_spec, shell=True)

    # First add all lemmas and axioms from aux
    spec_string = "\n"
    if aux is not None:
        for line in aux:
            spec_string += "\n" + line

    # Second add all completions as either assumptions or specs, and all integrity constraints as specs
    # First occurence of forall OR a word followed by iff starts completed definition
    # First occurence of forall OR a not starts an integrity constraint
    comp_exp = r'forall.*$|\w ?<->.+$'
    #cons_exp = r'forall.*\n|.*(not.+\n)'
    cons_exp = r'forall.*$|.*: ?(not.+$)'
    for line in completions:
        comp = re.search(comp_exp, line)
        cons = re.search(cons_exp, line)
        if comp:
            predicate = (re.search(r'of .*:', line)).group().strip(":")
            predicate = re.sub(r'of ', "", predicate)
            if predicate in privates_map.keys():
                spec = "assume: " + comp.group()
                spec_string += terminator(spec)
                inp = "input: " + privates_map[predicate]
                spec_string += terminator(inp)
            elif predicate in publics:
                spec = "spec: " + comp.group()
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

    # Replace all private predicates
    for predicate in privates_map.keys():
        spec_string = replace_predicate(privates_map, predicate, spec_string)
    with open(final_spec, "a") as f2:
        f2.write(spec_string)
    f2.close()
    return final_spec, publics

# Create a new alt program with renamed private predicates
def overwrite(path, publics):
    all_preds = get_preds_prog(path)
    for pred in publics:
        all_preds.discard(pred)
    privates = list(all_preds)
    mapping = renamed(privates, 2)
    with open(path, "r") as f:
        spec = f.read()
    f.close()
    for pred in privates:
        spec = replace_predicate(mapping, pred, spec)
    fp = path.split(".")[0] + "-renamed.lp"
    with open(fp, "w") as f:
        f.write(spec)
    f.close()
    sproc.run("chmod 666 " + fp, shell=True)
    return fp

# Verify lp against spec
def verify(lp_path, spec_path):
    try:
        anthem_output = sproc.run("./anthem verify-program " + lp_path + " " + spec_path, encoding='utf-8', stdout=sproc.PIPE, shell=True)
        anthem_output.check_returncode()
    except sproc.CalledProcessError:
        print("Error running anthem: ", anthem_output.stderr)
        sys.exit(1)
    print(anthem_output.stdout)

# Removes #show statements from input programs
def preprocess(fp):
    outp = []
    show_exp = r'^#show.*$'
    with open(fp, "r") as f:
        raw = f.readlines()
        for line in raw:
            if re.search(show_exp, line) is None:
                outp.append(line)
    f.close()
    newfp = "new-"+fp
    with open(newfp, "w") as f:
        f.writelines(outp)
    f.close()
    return newfp

# Extract the 'input: p/n' statements from the spec at fp
def get_inputs(fp):
    inputs = []
    inp_exp = r'^input:.+$'
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
        f.close()
        return inputs
    else:
        return None

if __name__ == "__main__":
    assert (sys.version_info >= (3, 6, 9)), "This script requires Python v3.6.9 (or later). Try python3"
    files, aux = parse_cmd()
    files["orig"] = preprocess(files["orig"])
    files["alt"] = preprocess(files["alt"])
    inputs = get_inputs(files["ctx"])
    print("Inputs from UG:")
    print(inputs)
    comp_fp, completions = generate_completion(files["orig"], inputs)
    if files["ctx"]:
        final_spec, public_preds = generate_spec(completions, files["ctx"], aux) 
    else:
        sproc.call("touch .spec", shell=True)
        final_spec, public_preds = generate_spec(completions, ".spec", aux)
    new_prog = overwrite(files["alt"], public_preds)
    print("")
    verify(new_prog, final_spec)
