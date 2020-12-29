import sys
import math

fp = open(sys.argv[1])

for l in fp:
    sl = l.split()

    if len(sl) == 4:
        x = float(sl[2])
        y = float(sl[3])

        a = math.degrees(math.atan2(y,x))

        if a < 0.0:
            a += 360.0

        print("%11.8f %11.8f %10.3f"%(x, y, a))
fp.close()