from Rtree import Rtree
from hilbert import HilbertRtree
import sys


def shooting_star(tree):
    if type(tree) is not HilbertRtree and type(tree) is not Rtree:
        raise TypeError('can only take HilbertRtree or Rtree as input')

    skyline = set()

    init = (sys.maxsize, sys.maxsize)

    T = set()

    T.add(init)

    while len(T) != 0:
        mx, my = T.pop()
        res = tree.bounded_NN_search(0, 0, mx, my, 0, 0, skyline)
        if res is not None:
            nx, ny = res
            T.add((nx, my))
            T.add((mx, ny))
            skyline.add(res)

    return skyline



