import json, sys
import subprocess as sproc


def success(answers, result):
    flag = True
    for name in result.keys():
        elem = result[name]
        ans_elem = answers[name]
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
    try:
        f = open(path + "-testing-result.txt", "w")
        command = "python3 anthem-p2p.py examples/" + path + "/" + path + ".1.lp examples/" + path + "/" + path + ".2.lp examples/" + path + "/" + path + ".ug "
        sproc.run(command, encoding='utf-8', stdout=f, shell=True)

        command = "python3 anthem-p2p.py examples/" + path + "/" + path + ".2.lp examples/" + path + "/" + path + ".1.lp examples/" + path + "/" + path + ".ug "
        sproc.run(command, encoding='utf-8', stdout=f, shell=True)
        f.close()

        f2 = open("examples/" + path + "/new-" + path + ".1.lp-summary.json")
        result1 = json.load(f2)
        f2.close()

        f2 = open("examples/" + path + "/new-" + path + ".2.lp-summary.json")
        result2 = json.load(f2)
        f2.close()
    except:
        print("Summary was not created.")
        sys.exit(1)

    if success(test_cases[path]["1"], result1):
        if success(test_cases[path]["2"], result2):
            print("success")
        else:
            print("fail")
    else:
        print("fail")
