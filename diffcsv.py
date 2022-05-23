import sys
import pandas

file1csv = ""
file2csv = ""

if len(sys.argv) != 3:
    print("usage: ", sys.argv[0], " file1.csv file2.csv ")
    exit(1)
else:
    file1csv = sys.argv[1]
    file2csv = sys.argv[2]

df1 = pandas.read_csv(file1csv, sep=';',)
df2 = pandas.read_csv(file2csv, sep=";")

colum = df1.columns

for idx, r1 in df1.iterrows():
  molname = r1["Objects"]
  r2 = df2[df2["Objects"] == molname]

  for j, v1 in  enumerate(list(r1.values)):
      v2 = r2.values[0][j]
      #print(v1, v2)
      if (v1 != v2):
          print(molname, v1, v2, colum[j])
