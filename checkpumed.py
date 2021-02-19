import pubchempy as pcp
import urllib.error

from rdkit import Chem

fp = open("publist.txt")

idx = 1
for l in fp:
    sl = l.split()
    if sl[1].isnumeric():
        try:
           result = pcp.get_compounds(sl[0], 'smiles')
           
           try:
               for r in result:
                   cid = r.to_dict()['cid']
                   if cid == int(sl[1]):
                       print(idx, ' - CID is equal ', cid , flush=True)
                   else:
                       print(idx, ' - ', cid, ' differ from ', sl[1], flush=True)
           except TypeError:
           
               try:
                   cidsearch = pcp.Compound.from_cid(int(sl[1]))
           
                   #cans = Chem.MolToSmiles(Chem.MolFromSmiles(sl[0]), True)
           
                   print(idx, ' - ',cidsearch.to_dict()['canonical_smiles'], ' vs ',
                       sl[0], ' cid ' , sl[1], flush=True)

               except urllib.error.HTTPError:
                   print(idx, ' - Error ', sl[0], sl[1], flush=True)
               except pcp.BadRequestError:
                   print(idx, ' - Error ', sl[0], sl[1], flush=True)

        except urllib.error.HTTPError:
            print(idx, ' - Error ', sl[0], sl[1], flush=True)
        except pcp.BadRequestError:
            print(idx, ' - Error ', sl[0], sl[1], flush=True)

    idx = idx + 1
