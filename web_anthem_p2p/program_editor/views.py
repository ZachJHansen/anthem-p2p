import json, sys, re
import subprocess as sproc
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from .forms import InputForm, OutputForm

def home(request):
    context = {}
    context['form'] = InputForm()
    return render(request, "program_editor/home.html", context)

def verify(request):
    if request.method == "POST":
        rp = request.POST
        form = InputForm(rp)
        if form.is_valid():
            outp = run_anthem_p2p(form.cleaned_data)
        if re.search(r'\(not proven\)', outp):
            outp = outp + "\nBOTTOM LINE: AP2P was unable to find a proof of equivalence between the programs within the time limit."
        else:
            outp = outp + "\n BOTTOM LINE: AP2P found a proof of equivalence between the programs!"
        form = OutputForm({
            'time_limit': rp['time_limit'],
            'original_program': rp['original_program'],
            'alternative_program': rp['alternative_program'],
            'user_guide': rp['user_guide'],
            'helper_lemmas': rp['helper_lemmas'],
            'output': outp})
        return render(request, 'program_editor/result.html', {'form': form})

def run_anthem_p2p(raw_map):
    creation_time = re.sub(":", "-", datetime.now().strftime("%X%f"))
    orig_name = creation_time + "-orig.lp"                              # Create a temporary original program file
    with open(orig_name, "w") as f:
        f.writelines(raw_map["original_program"])
    f.close()
    alt_name = creation_time + "-alt.lp"                                # Create a temporary alternative program file
    with open(alt_name, "w") as f:
        f.writelines(raw_map["alternative_program"])
    f.close()
    ug_name = creation_time + "-ug.ug"                                  # Create a temporary user guide file 
    with open(ug_name, "w") as f:
        f.writelines(raw_map["user_guide"])
    f.close()
    lem_name = creation_time + "-lemmas.spec"                           # Create a temporary file for helper lemmas
    with open(lem_name, "w") as f:
        f.writelines(raw_map["helper_lemmas"])
    f.close()
    time_limit = 300
    try:
        tl = raw_map.get("time_limit", 30)
        if tl and tl.strip():
            time_limit = int(float(tl) * 60)
    except Exception as e:
        print("Enter time limit in minutes!")
        return("Invalid time limit. Please enter time limit in minutes.")
    command = "python3 ../anthem-p2p.py " + orig_name + " " + alt_name + " " + ug_name 
    command += " -l " + lem_name + " -t " + str(time_limit)
    try:
        ap2p_out = sproc.run(command, encoding='utf-8', stdout=sproc.PIPE, shell=True)  # Run anthem-p2p.py
        print(ap2p_out.stdout)
        ap2p_out.check_returncode()
        ret_code = 1
    except sproc.CalledProcessError:
        print("Error running anthem-p2p: ", ap2p_out.stderr)
        ret_code = 2
    sproc.call("rm " + orig_name, shell=True)
    sproc.call("rm " + alt_name, shell=True)
    sproc.call("rm " + ug_name, shell=True)
    sproc.call("rm " + lem_name, shell=True)
    sproc.call("rm new-*.lp", shell=True)
    sproc.call("rm temp-*.spec", shell=True)
    if ret_code != 1:
        print("Error running Anthem-P2P...")
    return refactor_output(ap2p_out.stdout)

def refactor_output(outp):
    final_output = ["Attempting to derive output predicates in the original program (_1) from the alternative program's predicate definitions (_2)..."] 
    for line in outp.split("\n"):
        presupp = re.search(r'(Presupposed .+$)', line)
        if presupp:
            final_output.append('\t' + presupp.group(1))
        elif re.search(r'Finished verification of specification from translated program', line):
            final_output.append("\tFinished deriving the original program from the alternative program")
            final_output.append("Attempting to derive output predicates in the alternative program (_2) from the original program's predicate definitions (_1)...")
        elif re.search(r'Finished verification of translated program from specification', line):
            final_output.append("\tFinished deriving the alternative program from the original program")
        else:
            failed_spec = re.search(r'(^.+Verifying spec:.+)(Verifying spec: .+ \(not proven\)$)', line)
            failed_lemma = re.search(r'(^.+Verifying lemma:.+)(Verifying lemma: .+ \(not proven\)$)', line)
            failed_comp = re.search(r'(^.+Verifying completed definition .+)(Verifying completed definition .+ \(not proven\)$)', line)
            if failed_lemma:
                final_output.append('\t  ' + failed_lemma.group(2) + "\n\t  Failed to prove the preceding lemma!")
            elif failed_spec:
                final_output.append('\t  ' + failed_spec.group(2) + "\n\t  Failed to prove the preceding spec!")
            else:
                if failed_comp:
                    final_output.append('\t  ' + failed_comp.group(2) + "\n\t Failed to prove the preceding completed definition!")
            succ_spec = re.search(r'(Verified spec: .+$)', line)
            succ_lemma = re.search(r'(Verified lemma: .+$)', line)
            succ_comp = re.search(r'(Verified completed definition .+$)', line)
            if succ_spec:
                final_output.append('\t  ' + succ_spec.group(1))
            elif succ_lemma:
                final_output.append('\t  ' + succ_lemma.group(1))
            else:
                if succ_comp:
                    final_output.append('\t  ' + succ_comp.group(1))
    return '\n'.join(final_output)


















