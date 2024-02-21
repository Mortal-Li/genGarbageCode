
import sys
import os
import shutil
import random
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--prefix", type=str, default="OBFU", help="prefix of class name")
parser.add_argument("-c", "--classnum", type=int, default=20, help="number of cpp class file")
parser.add_argument("-m", "--member", type=int, default=10, help="max number of member function in one class file")
parser.add_argument("-s", "--static", type=int, default=2, help="max number of static function in one class file")
args, unknow_args = parser.parse_known_args()

PRE_FIX = args.prefix
CLASS_NUM = args.classnum
MEMBER_FUNC_NUM = args.member
STATIC_FUNC_NUM = args.static

TARGET_DIR = "./" + PRE_FIX
FUNC_TYPES = ["val", "for", "whl", "ifl", "flt", "log"]

print("Gen %d Class %d Func %d Static" % (CLASS_NUM, MEMBER_FUNC_NUM, STATIC_FUNC_NUM))
print("---------------------------------------------------")

def genRandomChar(strCnt, nameLen):
    for i in range(nameLen):
        typ = random.choice([0, 1, 2])
        if typ == 0:
            strCnt += str(random.randrange(10))
        elif typ == 1:
            strCnt += chr(random.randrange(26) + ord('a'))
        elif typ == 2:
            strCnt += chr(random.randrange(26) + ord('A'))

    return strCnt

def genRandomClassName():
    random.seed()
    nameLen = random.randrange(8, 20)
    clsName = ""
    return genRandomChar(clsName, nameLen)

def genRandomFuncName():
    random.seed()
    nameLen = random.randrange(10, 20)
    funcName = "" + chr(random.randrange(26) + ord(nameLen >= 15 and 'a' or 'A'));
    return genRandomChar(funcName, nameLen)

def genFuncUnitContent(typ, nt, sfx):
    if typ == "val":
        return "%sint k%s = %d;\n%sk%s -= %d;\n\n" % (nt, sfx, random.randrange(100), nt, sfx, random.randrange(1, 5))
    elif typ == "flt":
        return "%sfloat e%s = %d;\n%se%s *= %d;\n\n" % (nt, sfx, random.randrange(200), nt, sfx, random.randrange(6, 10))
    elif typ == "for":
        return "%sint a%s = 0;\n%sfor (int i = 0; i < %d; ++i) {\n%s\ta%s += i;\n%s}\n\n" % (nt, sfx, nt, random.randrange(10, 40), nt, sfx, nt)
    elif typ == "whl":
        return "%sfloat f%s = 0;\n%swhile(f%s < %d) {\n%s\tf%s = f%s + %d;\n%s}\n\n" % (nt, sfx, nt, sfx, random.randrange(8, 16), nt, sfx, sfx, random.randrange(1, 3), nt)
    elif typ == "ifl":
        return "%sint myc%s = %d;\n%sbool isSmaller%s = false;\n%sif (myc%s < 50) {\n%s\tisSmaller%s = true;\n%s} else {\n%s\tisSmaller%s = false;\n%s}\n\n" % \
        (nt, sfx, random.randrange(100), nt, sfx, nt, sfx, nt, sfx, nt, nt, sfx, nt)
    elif typ == "log":
        return "%scout<<\"log %s\"<<endl;\n\n" % (nt, sfx)
    
    print("FUNC TYPE ERROR!")
    sys.exit()

def genRandomFuncContent():
    cnt = ""
    for i in range(2, 10):
        cc = random.choice(FUNC_TYPES)
        cnt += genFuncUnitContent(cc, "\t", str(i))

    return cnt

def genRandomStaticFuncContent():
    return genFuncUnitContent(random.choice(FUNC_TYPES), "\t\t", str(random.randrange(10)))

def genFile(clsName, strCnt, isHead):
    with open(clsName + (isHead and ".h" or ".cpp"), "w") as f:
        f.write(strCnt)
        f.flush()

def makeClassFile(clsName):
    headCnt = "class %s {\npublic:\n" % (clsName)
    cppCnt = "#include<iostream>\n#include \"%s.h\"\n\nusing namespace std;\n\n" % (clsName)

    for i in range(random.randint(1, MEMBER_FUNC_NUM)):
        funcName = genRandomFuncName()
        headCnt += "\tvoid %s();\n" % (funcName)
        cppCnt += "void %s::%s()\n{\n" % (clsName, funcName)
        cppCnt += genRandomFuncContent()
        cppCnt += "}\n\n"

    headCnt += "\npublic:\n";

    for i in range(random.randint(1, STATIC_FUNC_NUM)):
        funcName = "s_" + genRandomFuncName()
        headCnt += "\tstatic int %s() {\n" % (funcName)
        headCnt += genRandomStaticFuncContent()
        headCnt += "\t\treturn %d;\n" % (i)
        headCnt += "\t}\n"

    headCnt += "};"
    genFile(clsName, headCnt, True)
    genFile(clsName, cppCnt, False)

def goRun():
    if os.path.exists(os.path.join(os.getcwd(), TARGET_DIR)):
        shutil.rmtree(TARGET_DIR)
    os.mkdir(TARGET_DIR)
    os.chdir(os.path.join(os.getcwd(), TARGET_DIR))
    
    for i in range(CLASS_NUM):
        clsName = PRE_FIX + genRandomClassName()
        makeClassFile(clsName)
        # print(clsName)
    
    # insertCodeToProj()

    print("\n--------------> Done!\n")

if __name__ == "__main__":
    goRun()
