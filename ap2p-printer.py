import json, argparse, atexit
import subprocess as sproc
from program import *

debug = False
verbose_flag = False
global_summary = {"assumptions": [], "specs": []}
files = {"orig": None, "alt": None, "spec": None}

# Parse the optional spec file, return
# a string containing helper lemmas
def parse_lemmas(fname):
    aux = []
    if fname is not None:
        spec_exp = r'.*.spec'
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
    try:
        parser = argparse.ArgumentParser("Anthem-P2P", "Verifies the equivalent external behavior of two logic programs.")
        parser.add_argument("lp", nargs=2, help="Logic programs")
        parser.add_argument("ug", nargs=1, help="A .ug file defining the context (user guide)")
        parser.add_argument("-l", "--lemmas", required=False, dest="aux", help="Lemmas and axioms to accelerate proof search")
        parser.add_argument("-t", "--time-limit", required=False, dest="time", help="Time limit for Vampire")
        parser.add_argument("-v", "--verbose", required=False, dest="verbose", help="Extra error messages (y/n)")
        args = parser.parse_args()
    except Exception as e:
        print(e)
        sys.exit(1)
    files["orig"], files["alt"], files["ctx"] = args.lp[0], args.lp[1], args.ug[0]
    aux = parse_lemmas(args.aux)
    if args.verbose == "y":
        global verbose_flag
        verbose_flag = True
    # Sanity Check
    if not re.search(r'.*.lp$', files["orig"]):
        print("Error (1) parsing program arguments: expects 2 files with .lp extension, and 1 file with a .ug extension")
        sys.exit(1)
    if not re.search(r'.*.lp$', files["alt"]):
        print("Error (2) parsing program arguments: expects 2 files with .lp extension, and 1 file with a .ug extension")
        sys.exit(1)
    if not re.search(r'.*.ug$', files["ctx"]):
        print("Error (3) parsing program arguments: expects 2 files with .lp extension, and 1 file with a .ug extension")
        sys.exit(1)
    if verbose_flag:
        print("\n####### Input Files (Original, Alternative, Context) #######")
        print(files)
        print("")
    return aux, args.time

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
        if verbose_flag:
            print("####### Input predicates from UG: #######")
            print(inputs)
            print("\n####### Output predicates from UG: #######")
            print(outputs)
        return inputs, outputs
    else:
        print("Fatal error")
        sys.exit(1)


def syntax_check(fp):
    try:
        command = 'clingo ' + fp
        clingo_check = sproc.run(command, encoding='utf-8', stdout=sproc.PIPE, stderr=sproc.PIPE, shell=True)
        clingo_check.check_returncode()
    except sproc.CalledProcessError as e:
        if e.returncode == 65:
            if re.search(r'parsing failed', clingo_check.stderr):
                print("Syntax error in ", fp)
                sys.exit(1)

# Create a Program instance, rename private predicates
# within it, remove directives and comments, write the
# resulting program to a new file
def preprocess(fp, name, addendum, inputs, outputs):
    syntax_check(fp)
    try:
        with open(fp, "r") as f:
            program = Program(name, f.readlines(), verbose_flag)
        f.close()
        program.rename_predicates(inputs, outputs, addendum)
        path = "/".join(fp.split("/")[0:-1])
        if len(path) != 0:
            newfp = path + "/new-" + fp.split("/")[-1]                                                   # Write to new file
        else:
            newfp = "new-" + fp
        program.print_program(newfp)
    except Exception as e:
        print("Error preprocessing file", fp)
        print(e)
        sys.exit(1)
    syntax_check(newfp)
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
        anthem_output = sproc.run(command, encoding='utf-8', stdout=sproc.PIPE, stderr=sproc.PIPE, shell=True)
        anthem_output.check_returncode()
    except sproc.CalledProcessError:
        print("Error running anthem: ", anthem_output.stderr)
        sys.exit(1)
    exp = r'completed definition of.+\n|integrity constraint:.+'
    completions = re.findall(exp, anthem_output.stdout)
    sproc.call("rm " + empty_spec, shell=True)
    # Pass completed definitions back to main
    return completions

def add_completion(comp, renamed_privates, program, spec_string):
    predicate = comp.group(1)
    if predicate in renamed_privates:
        if verbose_flag:
            print("\tCompleted definition of renamed private predicate", predicate, "is being added as an input and assumption to the final specification.")
        global_summary["assumptions"].append(predicate) 
        spec = "assume: " + comp.group(2)
        spec_string += terminator(spec)
        inp = "input: " + predicate
        spec_string += terminator(inp)
    elif predicate in program.outputs:
        if verbose_flag:
            print("\tCompleted definition of output predicate", predicate, "is being added as a spec to the final specification.")
        global_summary["specs"].append(predicate) 
        spec = "spec: " + comp.group(2)
        spec_string += terminator(spec)
    elif predicate in program.inputs:
        print("\tCompleted definition of an input predicate is illegal. Predicate:", predicate)
        sys.exit(1)
    else:
        print("Unknown predicate: ", predicate)
        sys.exit(1)
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
    if cons.group(1) is None:
        match = cons.group(2)
    else:
        match = cons.group(1)
    if verbose_flag:
        print("\tConstraint", match, "is being added as a spec to the final specification.")
    spec = "spec: " + match
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
    prop_cons_exp = r'constraint.*: ?(not.+$)|definition.*: ?(not.+$)'
    if verbose_flag:
        print("\nConstructing final specification...")
    for line in completions:
        fo_comp = re.search(fo_comp_exp, line)
        prop_comp = re.search(prop_comp_exp, line)
        fo_cons = re.search(fo_cons_exp, line)
        prop_cons = re.search(prop_cons_exp, line)
        if fo_comp:
            spec_string = add_completion(fo_comp, renamed_privates, orig, spec_string)
        elif prop_comp:
            spec_string = add_completion(prop_comp, renamed_privates, orig, spec_string)
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


def cleanup():
    if files["orig"]:
        sproc.call("rm " + files["orig"], shell=True)
    if files["alt"]:
        sproc.call("rm " + files["alt"], shell=True)
    if files["spec"]:
        sproc.call("rm " + files["spec"], shell=True)

# Verify lp against spec
def verify(lp_path, spec_path, time_limit, simplify=True):
    success = True
    forward, backward = True, True
    direction = "forward"
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')                                    # Remove the ANSI escape characters
    if simplify:
        command = "./anthem verify-program " + lp_path + " " + spec_path
    else:
        command = "./anthem verify-program --no-simplify " + lp_path + " " + spec_path
    if time_limit is not None:
        command += " --time-limit " + str(time_limit)
    error_log = ''
    with sproc.Popen(command, stdout=sproc.PIPE, stderr=sproc.STDOUT, bufsize=1, universal_newlines=True, shell=True) as p:
        print("Attempting to derive completed definitions in the original program (_1) from completed definitions in the alternative program (_2)...")
        for line in p.stdout:
            presupp = re.search(r'(Presupposed .+$)', line)
            if presupp:
                print('  ' + presupp.group(1))
            elif re.search(r'Finished verification of specification from translated program', line):
                if forward:
                    print("  Finished deriving the original program from the alternative program")
                else:
                    print("  Unable to derive the original program from the alternative program")
                    success = False
                direction = "backward"
                print("\nAttempting to derive completed definitions in the alternative program (_2) from completed definitions in the original program (_1)...")
            elif re.search(r'Finished verification of translated program from specification', line):
                if backward:
                    print("  Finished deriving the alternative program from the original program")
                else:
                    print("  Unable to derive the alternative program from the original program")
                    success = False
            elif re.search(r'ERROR anthem', line):
                error_log = error_log + line
                success = False
            else:
                line = ansi_escape.sub('@', line)
                verifying_verified  = re.search(r'^@\s*Verifying .+:.+@@\s*(Verified .+: .+in [0-9]+\.[0-9]+ seconds)$', line)       # Successful
                verifying_verifying = re.search(r'^@\s*Verifying .+:.+@@\s*Verifying (.+: .+)\(not proven\)$', line)                 # Failed
                if verifying_verified:
                    print("  ", verifying_verified.group(1))
                elif verifying_verifying:
                    print("    Failed to verify", verifying_verifying.group(1))
                    if direction == "forward":
                        forward = False                                                             # Forward direction failed
                    else:
                        backward = False                                                            # Backward direction failed
                else:
                    verifying_only = re.search(r'^@\s*(Verifying .+:.+)@@$', line)
                    verified_only  = re.search(r'^Verified (.+:.+$)', line)
                    if verified_only:
                        if re.search(r'Verified .+: .+in [0-9]+\.[0-9]+ seconds', line):
                            print("    ", line)
                        elif re.search('\(not proven\)$', line):
                            print("    Failed to verify", verified_only.group(1))
                            if direction == "forward":
                                forward = False                                                             # Forward direction failed
                            else:
                                backward = False                                                            # Backward direction failed
                    if verifying_only:
                        print("\t", verifying_only.group(1))
        return_code = p.wait()
        if return_code:
            print(error_log)
            raise sproc.CalledProcessError(return_code, command)
            sys.exit(1)
        return success

if __name__ == "__main__":
    assert (sys.version_info >= (3, 6, 9)), "This script requires Python v3.6.9 (or later). Try python3"
    #atexit.register(cleanup)
    try:
        clingo_check = sproc.run('clingo --version', encoding='utf-8', stdout=sproc.PIPE, stderr=sproc.PIPE, shell=True)
        clingo_check.check_returncode()
    except sproc.CalledProcessError:
        print("Error running clingo! Is it installed?")
        sys.exit(1)
    aux, time = parse_cmd()
    inputs, outputs = get_ug_preds(files["ctx"])
    files["orig"], orig = preprocess(files["orig"], "orig", 1, inputs, outputs)
    files["alt"], alt = preprocess(files["alt"], "alt", 2, inputs, outputs)
    global_summary["privates"] = list(orig.privates)
    global_summary["publics"] = list(orig.inputs.union(orig.outputs))
    completions = generate_completion(files["orig"], inputs, True)
    if verbose_flag:
        print("\n####### Completions #######")
        for c in completions:
            print(c)
    if files["ctx"]:
        final_spec = generate_spec(completions, files["ctx"], orig, aux) 
    else:
        sproc.call("touch .spec", shell=True)
        final_spec = generate_spec(completions, ".spec", orig, aux) 
    files["spec"] = final_spec
    print(final_spec)
    print("Exiting system early on purpose - email Zach")
    sys.exit(1)
    success = verify(files["alt"], final_spec, time, True)
    if success:
        print("BOTTOM LINE: AP2P found a proof of equivalence between the programs!\n")
        global_summary["equiv"] = "Equivalent"
    else:
        #print("\n\nTrying again without simplification...\n\n")
        global_summary["equiv"] = "Not"
        print("BOTTOM LINE: AP2P was unable to find a proof of equivalence between the programs within the time limit.\n")
    if debug:
        with open(files["orig"]+"-summary.json", "w") as f:
            json.dump(global_summary, f)
        f.close()

