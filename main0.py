import csv
import time
import sys

from hilbert import HilbertRtree
from Rtree import Rtree
from shooting_star import shooting_star

rtree = Rtree(8)
htree = HilbertRtree(8)
print("constructing trees...")
lst = list()
with open("island2d63383.csv") as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        num0 = int(round(float(row[0])))
        num1 = int(round(float(row[1])))

        rtree.insert(num0, num1)
        htree.insert(num0, num1)
        lst.append((num0, num1))

print('searching skyline using brute-force ...')
total = 0
ans = None
for _ in range(0, 5):
    t3 = time.time()
    ans = list()
    for p in lst:
        flag = True
        for q in lst:
            if q[0] < p[0] and q[1] < p[1]:
                flag = False
                break
        if flag:
            ans.append(p)
    t4 = time.time()
    total += t4 - t3
    print("time lapsed:" + str(t4 - t3))
print(ans)
print("avg: " + str(total / 5))

print('searching skyline using R-tree ...')
total = 0
for _ in range(0, 5):
    t0 = time.time()
    ans0 = shooting_star(htree)
    t1 = time.time()
    print("runtime: " + str(t1 - t0))
    total += t1 - t0
total /= 5
print("avg: " + str(total))

print('searching skyline using Hilbert R-tree ...')
total = 0
for _ in range(0, 5):
    t0 = time.time()
    ans1 = shooting_star(htree)
    t1 = time.time()
    print("runtime: " + str(t1 - t0))
    total += t1 - t0
total /= 5
print("avg: " + str(total))
