import re

def replace_predicate_old(mapping, pred, spec):
    pname = pred.split("/")[0]                                      # Extract p from p/n
    arity = pred.split("/")[1]                                      # Extract n from p/n
    new_name = mapping[pred].split("/")[0]                          # Extract p_1 from p_1/n
    if int(arity) > 0:
        base_exp = r'\W' + pname + r'\(|^' + pname + r'\('           # Match non-word strings followed by pname(, or pname(
    else:
        base_exp = r'\W' + pname + r'\W|^' + pname + r'\W'                     # Match 1 non-word char or string start followed by pname
    base_exp = re.compile(base_exp)
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
        base_exp = r'\W' + pname + r'\W|^' + pname + r'\W'          # Match pname
    occs = re.findall(base_exp, spec)                               # Find matching substrings
    renamed = [re.sub(pname, new_name, o) for o in occs]            # Replace the predicate name within each matched substring
    replace_map = dict(zip(occs, renamed))
    print(replace_map)
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

line = "completed definition of q/0: q <-> p\n"
comp_exp = r'definition of +(.+): *(forall.*$)|definition of +(.+): *(\w+ ?<->.+$)'
comp_exp = r'definition of +(.+): *(\w+ ?<->.+$)'
comp = re.search(comp_exp, line)
print(comp.group(1))
print(comp.group(2))












