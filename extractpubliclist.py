import os
import sys
import glob
import tempfile
import subprocess

import pathlib

path = ""

if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    print ("Usage: ", sys.argv[0] , " path ")
    exit(1)


for name in glob.glob(path+"*.sdf"): 
    nname = name.replace(path, "")
    nname = nname.replace(".sdf", "")

    if (nname.find("CHEMBL") >= 0) or \
        (nname.find("ZINC") >= 0) or \
         nname.isnumeric():
        
        temp_name = next(tempfile._get_candidate_names())

        abspath = pathlib.Path(__file__).parent.absolute()

        toexe = "obabel  -isdf "+str(abspath)+"/"+name+" -osmi -O "+temp_name
        results  = subprocess.run(toexe, shell=True, check=True, \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, \
            universal_newlines=True)

        fp = open(temp_name, "r")
        smilename = fp.readline()
        fp.close()

        os.remove(temp_name) 

        print(smilename, end="")