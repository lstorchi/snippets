import subprocess 
import os

import pandas as pd

from Bio.PDB.PDBParser import PDBParser

def get_atomscount (filename):

    parser=PDBParser(PERMISSIVE=1)

    structure = parser.get_structure("singelemodel", filename)

    atomscounter = {}

    for model in structure:
        for chain in model:
            for residue in chain:
                for a in residue:
                    an = a.get_name()

                    if an in atomscounter:
                        atomscounter[an] += 1
                    else:
                        atomscounter[an] = 1

    return atomscounter

fp = open("publist_checkout.txt", "r")

for l in fp:

    if l.find(" vs ") > 0:
        sl = l.split()

        if len(sl) == 7:
            smi1 = sl[2]
            smi2 = sl[4]

            fpo = open("1.smi", "w")
            fpo.write(smi1)
            fpo.close()

            fpo = open("2.smi", "w")
            fpo.write(smi2)
            fpo.close()

            try:
                toexe = "obabel --gen3d -ismi 1.smi -opdb -O 1.pdb"
                results  = subprocess.run(toexe, shell=True, check=True, \
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, \
                    universal_newlines=True)
                toexe = "obabel --gen3d -ismi 2.smi -opdb -O 2.pdb" 
                results  = subprocess.run(toexe, shell=True, check=True, \
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, \
                    universal_newlines=True)

                toexe = "python3 isoRMSD.py -r 1.pdb -p 2.pdb"
                results  = subprocess.run(toexe, shell=True, check=True, \
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, \
                    universal_newlines=True)

                df = pd.read_csv("rmsd.csv")

                an1 = get_atomscount ("1.pdb")
                an2 = get_atomscount ("2.pdb")

                differ = 0
                for n in an1:
                    if (an1[n] != an2[n]):
                        differ += 1

                print("%10.5f %5d "%(df["RMSD_Align"].values[0], differ))

                os.remove("rmsd.csv")

            except subprocess.CalledProcessError:
                print("Error ", smi1, " vs " , smi2)

            os.remove("1.smi") 
            os.remove("2.smi") 
            os.remove("1.pdb") 
            os.remove("2.pdb") 
        else:
            print("ERROR")
            exit(1)
