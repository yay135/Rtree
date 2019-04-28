from Rtree import Rtree
from hilbert import HilbertRtree
from shooting_star import shooting_star
import time
import random


def main0():
    tree = Rtree(10)
    htree = HilbertRtree(10)
    lst = set()
    print("generating random points...")
    for _ in range(0, 100000):
        x = random.randint(1, 10000000)
        y = random.randint(1, 10000000)
        p = (x, y)
        lst.add(p)
    # for _ in range(0, 200000):
    #     x = random.randint(400000, 600000)
    #     y = random.randint(400000, 600000)
    #     p = (x, y)
    #     lst.add(p)
    #
    # for _ in range(0, 200000):
    #     x = random.randint(800000, 10000000)
    #     y = random.randint(800000, 10000000)
    #     p = (x, y)
    #     lst.add(p)
    print("searching skyline 5 times using brute-force...")
    total = 0
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

    print("constructing trees...")
    for p in lst:
        tree.insert(p[0], p[1])
    htree.insert_list(lst)
    print("calculating skyline 5 times using R-tree...")
    total = 0
    for _ in range(0, 5):
        t0 = time.time()
        ans0 = shooting_star(tree)
        t1 = time.time()
        total += t1 - t0
        print("time lapsed:" + str(t1 - t0))
        print(ans0)
    print("avg: " + str(total/5))
    print("calculating skyline 5 times using Hilbert R-tree...")
    total = 0
    for _ in range(0, 5):
        t1 = time.time()
        ans1 = shooting_star(htree)
        t2 = time.time()
        total += t2 - t1
        print("time lapsed:" + str(t2 - t1))
        print(ans1)
    print("avg: " + str(total / 5))

main0()