import json
import subprocess as sproc


def success(answers, r1, r2):
    flag = True
    for name in r1.keys():
        elem = r1[name]
        ans_elem = answers[name + "1"]
        if isinstance(ans_elem, list):
            elem.sort()
            ans_elem.sort()
        if ans_elem != elem:
            flag = False
    for name in r2.keys():
        elem = r2[name]
        ans_elem = answers[name + "2"]
        if isinstance(ans_elem, list):
            elem.sort()
            ans_elem.sort()
        if ans_elem != elem:
            flag = False
    return flag

with open("test-cases.json", "r") as f:
    test_cases = json.load(f)
f.close()

for path in test_cases.keys():
    f = open(path + "-testing-result.txt", "w")
    command = "python3 anthem-p2p.py examples/" + path + "/" + path + ".1.lp examples/" + path + "/" + path + ".2.lp examples/" + path + "/" + path + ".ug "
    sproc.run(command, encoding='utf-8', stdout=f, shell=True)

    command = "python3 anthem-p2p.py examples/" + path + "/" + path + ".2.lp examples/" + path + "/" + path + ".1.lp examples/" + path + "/" + path + ".ug "
    sproc.run(command, encoding='utf-8', stdout=f, shell=True)
    f.close()

    f2 = open("examples/" + path + "/" + path + ".1.lp")
    result1 = json.load(f2)
    f2.close()

    f2 = open("examples/" + path + "/" + path + ".2.lp")
    result2 = json.load(f2)
    f2.close()

    if success(test_cases[path], result1, result2):
        print("success")
    else:
        print("fail")
