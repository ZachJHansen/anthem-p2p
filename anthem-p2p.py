import json
import subprocess as sproc
from program import *

global_summary = {"assumptions": [], "specs": []}

# Parse the optional spec file, return
# a string containing helper lemmas
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

# Identify lp, ug and spec files from command line input
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

# Create a Program instance, rename private predicates
# within it, remove directives and comments, write the
# resulting program to a new file
def preprocess(fp, name, addendum, publics):
    with open(fp, "r") as f:
        program = Program(name, f.readlines())
    f.close()
    program.rename_predicates(publics, addendum)
    path = "/".join(fp.split("/")[0:-1])
    if len(path) != 0:
        newfp = path + "/new-" + fp.split("/")[-1]                                                   # Write to new file
    else:
        newfp = "new-" + fp
    program.print_program(newfp)
    return newfp, program

# Run Anthem (forward direction) on the lp at fp against a 
# specification containing the input statements from the user guide
def generate_completion(fp, inputs, simplify=True):
    # Create a temporary specification file
    name = fp.split("/")[-1].strip()
    name = name.replace(".lp", "-completion.spec")
    empty_spec = "temp-" + name
    spec_gen_output = sproc.run("touch " + empty_spec, shell=True)
    if inputs is not None:
        with open(empty_spec, "w") as f:
            for pred in inputs:
                f.write("input: " + pred + ".\n")
        f.close()
    # Run Anthem
    if simplify:
        command = "./anthem verify-program --proof-direction=forward " + fp + " " + empty_spec
    else:
        command = "./anthem verify-program --proof-direction=forward --no-simplify " + fp + " " + empty_spec
    try:
        anthem_output = sproc.run(command, encoding='utf-8', stdout=sproc.PIPE, shell=True)
        anthem_output.check_returncode()
    except sproc.CalledProcessError:
        print("Error running anthem: ", anthem_output.stderr)
        sys.exit(1)
    exp = r'completed definition of.+\n|integrity constraint:.+'
    completions = re.findall(exp, anthem_output.stdout)
    sproc.call("rm " + empty_spec, shell=True)
    # Pass completed definitions back to main
    return completions

def add_completion(comp, renamed_privates, publics, spec_string):
    predicate = comp.group(1)
    if predicate in renamed_privates:
        print("\tCompleted definition of renamed private predicate", predicate, "is being added as an input and assumption to the final specification.")
        global_summary["assumptions"].append(predicate) 
        spec = "assume: " + comp.group(2)
        spec_string += terminator(spec)
        inp = "input: " + predicate
        spec_string += terminator(inp)
    elif predicate in publics:
        print("\tCompleted definition of public predicate", predicate, "is being added as a spec to the final specification.")
        global_summary["specs"].append(predicate) 
        spec = "spec: " + comp.group(2)
        spec_string += terminator(spec)
    else:
        # maybe an error (condition 3 of refactoring draft)
        print("Unknown predicate: ", predicate)
    return spec_string

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

def add_constraint(cons, spec_string):
    print("\tConstraint", cons.group(1), "is being added as a spec to the final specification.")
    spec = "spec: " + cons.group(1)
    spec_string += terminator(spec)
    return spec_string

def generate_spec(completions, context_path, orig, aux):
    # Final spec should combine the completed definitions with the context at context_path
    # Don't change the original context (user guide), just create a new, extended version
    # Use the renamed private predicates 
    final_spec = re.sub(".ug", "-final.spec", context_path)
    spec_gen_output = sproc.run("cp " + context_path + " " + final_spec, shell=True)
    sproc.run("chmod oug+rw " + final_spec, shell=True)
    renamed_privates = []
    for original_pred in orig.privates:
        pname, arity = original_pred.split("/")
        renamed_privates.append(pname + "_1/" + arity)

    # First add all lemmas and axioms from aux
    spec_string = "\n"
    if aux is not None:
        for line in aux:
            spec_string += "\n" + line

    # Second add all completions as either assumptions or specs, and all integrity constraints as specs
    # First occurence of forall OR a word followed by iff starts completed definition
    # First occurence of forall OR a not starts an integrity constraint
    fo_comp_exp = r'definition of +(.+): *(forall.*$)'
    prop_comp_exp = r'definition of +(.+): *(\w+ ?<->.+$)'
    fo_cons_exp = r'constraint.+(forall.*$)'
    prop_cons_exp = r'constraint.+.*: ?(not.+$)'
    print("\nConstructing final specification...")
    for line in completions:
        fo_comp = re.search(fo_comp_exp, line)
        prop_comp = re.search(prop_comp_exp, line)
        fo_cons = re.search(fo_cons_exp, line)
        prop_cons = re.search(prop_cons_exp, line)
        if fo_comp:
            spec_string = add_completion(fo_comp, renamed_privates, orig.publics, spec_string)
        elif prop_comp:
            spec_string = add_completion(prop_comp, renamed_privates, orig.publics, spec_string)
        elif fo_cons:
            spec_string = add_constraint(fo_cons, spec_string)
        elif prop_cons:
            spec_string = add_constraint(prop_cons, spec_string)
        else:
            print("Parsing error: couldn't find a completed definition or an integrity constraint in:")
            print(line)
            sys.exit(1)

    print("")
    with open(final_spec, "a") as f2:
        f2.write(spec_string)
    f2.close()
    return final_spec

# Verify lp against spec
def verify(lp_path, spec_path, simplify=True):
    if simplify:
        command = "./anthem verify-program " + lp_path + " " + spec_path
    else:
        command = "./anthem verify-program --no-simplify " + lp_path + " " + spec_path
    try:
        anthem_output = sproc.run(command, encoding='utf-8', stdout=sproc.PIPE, shell=True)
        anthem_output.check_returncode()
    except sproc.CalledProcessError:
        print("Error running anthem: ", anthem_output.stderr)
    print(anthem_output.stdout)
    fail = r'\(not proven\)'
    if re.search(fail, anthem_output.stdout):
        return False
    else:
        return True

if __name__ == "__main__":
    assert (sys.version_info >= (3, 6, 9)), "This script requires Python v3.6.9 (or later). Try python3"
    files, aux = parse_cmd()
    inputs, outputs = get_ug_preds(files["ctx"])
    public_preds = list(set(inputs + outputs))
    files["orig"], orig = preprocess(files["orig"], "orig", 1, public_preds)
    files["alt"], alt = preprocess(files["alt"], "alt", 2, public_preds)
    global_summary["privates"] = list(orig.privates)
    global_summary["publics"] = list(orig.publics)
    completions = generate_completion(files["orig"], inputs, False)
    if files["ctx"]:
        final_spec = generate_spec(completions, files["ctx"], orig, aux) 
    else:
        sproc.call("touch .spec", shell=True)
        final_spec = generate_spec(completions, ".spec", orig, aux) 
    success = verify(files["alt"], final_spec, False)
    if success:
        global_summary["equiv"] = "Equivalent"
    else:
        #print("\n\nTrying again without simplification...\n\n")
        global_summary["equiv"] = "Not"
    with open(files["orig"]+"-summary.json", "w") as f:
        json.dump(global_summary, f)
    f.close()
