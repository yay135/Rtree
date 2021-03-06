import sys
from hilbertcurve.hilbertcurve import HilbertCurve


class HilbertRtree:
    # a two-dimension Rtree example
    # a node in Rtree can only contain up to degree points
    # can only insert bb
    class Point:
        # a point contains two-dimensional value
        def __init__(self, x, y):
            if x < 0 or y < 0:
                raise ValueError("point can only not have negative dimension values")
            self.x = x
            self.y = y

    class BB:
        # dlp down left point
        # urp up right point
        def __init__(self, point0, point1):
            if point1.x < point0.x or point1.y < point0.y:
                raise ValueError("point0 should be on the down left of point1")
            # down left point of the bb
            self.dlp = point0
            # up right point of the bb
            self.urp = point1
            self.hv = None

    class Node:
        def __init__(self, degree, lst=None, map=None):
            if not type(degree) is int:
                raise TypeError("can only accept int and list of bbs and dict")

            if lst is not None and not type(lst) is list:
                raise TypeError("can only accept int and list of bbs and dict")

            if map is not None and not type(map) is dict:
                raise TypeError("can only accept int and list of bbs and dict")

            # degree of the node is the max number of bb in the node
            self.max_len = degree
            # bb container
            if lst is None:
                self.lst = list()
            else:
                self.lst = lst
            # bb to node map
            if map is None:
                self.map = dict()
            else:
                self.map = map

            self.LHV = 0
            # update the LHV
            self.update_LHV()

        def update_LHV(self):
            # update the LHV for each node
            for bb in self.list_bb():
                self.LHV = max(self.LHV, bb.hv)

        def append(self, bb, n=None):
            # node can only accept bounding box
            if not type(bb) is HilbertRtree.BB:
                raise TypeError("node can only accept bounding box")

            if len(self.lst) < self.max_len:
                self.lst.append(bb)
                if n is not None:
                    self.map[bb] = n
                # insert bb successfully
                # update largest hilbert value of a node
                self.LHV = max(self.LHV, bb.hv)
                return True
            else:
                # insert bb failed
                return False

        def remove(self, i):
            # remove bb from node at index i
            # i must be int
            if not type(i) is int:
                raise TypeError("index to remove should be int")
            if i < 0 or i > len(self.lst):
                raise ValueError("index is not in node range")

            bb = self.lst.pop(i)
            if bb in self.map:
                del self.map[bb]
            # update the LHV
            self.update_LHV()

        def list_bb(self):
            # return current copy of list of bb
            return self.lst

        def replace_with(self, i, bb):
            if self.lst[i] == bb:
                return
            # change an bb in the node
            if self.lst[i] in self.map:
                self.map[bb] = self.map[self.lst[i]]
                del self.map[self.lst[i]]

            self.lst[i] = bb
            # update largest LHV
            self.update_LHV()

        def split(self):
            # split the list into two ( 7 -> 3,4, 8->4,4)
            l = len(self.lst)
            l_lst, r_lst = self.lst[:l // 2], self.lst[l // 2:]

            l_dict, r_dict = dict(), dict()
            for item in l_lst:
                if item in self.map:
                    l_dict[item] = self.map[item]

            for item in r_lst:
                if item in self.map:
                    r_dict[item] = self.map[item]

            return HilbertRtree.Node(self.max_len, l_lst, l_dict), HilbertRtree.Node(self.max_len, r_lst, r_dict)

    # a two-dimension Rtree example
    # a node in Rtree can only contain up to degree points
    def __init__(self, degree):
        if not type(degree) is int:
            raise TypeError("degree should be int")
        if degree < 2:
            raise TypeError('degree should not less 1')
        self.degree = degree
        self.root = None
        self.hilbertCurve = HilbertCurve(128, 2)

    def get_hv(self, bb):
        # calculate the hilbert value for the bounding box
        # hilbert value of a rectangular is defined as the hilbert value of its center coordinates
        if type(bb) is not HilbertRtree.BB:
            raise TypeError("can only calculate hv over BB")

        mid_x = (bb.dlp.x + bb.urp.x)//2
        mid_y = (bb.dlp.y + bb.urp.y)//2

        h = self.hilbertCurve.distance_from_coordinates([mid_x, mid_y])
        return h

    def genBB(self, lst):
        # create new bounding box for points or for BBs
        min_x = sys.maxsize
        min_y = sys.maxsize
        max_x = 0
        max_y = 0

        for item in lst:

            if not type(item) is self.BB and not type(item) is self.Point:
                raise TypeError("item passed in shoud be Point or BB")

            if type(item) is self.Point:
                min_x = min(min_x, item.x)
                min_y = min(min_y, item.y)

                max_x = max(max_x, item.x)
                max_y = max(max_y, item.y)

            elif type(item) is self.BB:
                min_x = min(item.dlp.x, min_x)
                min_y = min(item.dlp.y, min_y)

                max_x = max(max_x, item.urp.x)
                max_y = max(max_y, item.urp.y)

        bb = self.BB(self.Point(min_x, min_y), self.Point(max_x, max_y))
        bb.hv = self.get_hv(bb)
        return bb

    def is_internal_node(self, n):
        # decide whether this node is internal node or not.
        if type(n) is self.Node:
            return len(n.map) != 0
        else:
            raise TypeError("can only take type Node as input")

    def is_completely_cover(self, bb0, bb1):

        if not type(bb0) is self.BB or not type(bb1) is self.BB:
            raise TypeError("can only take type BB as input")
        # return whether bb0 is completely covered by bb1
        return bb0.dlp.x >= bb1.dlp.x and bb0.dlp.y >= bb1.dlp.y and bb0.urp.x <= bb1.urp.x and bb0.urp.y <= bb1.urp.y

    def get_size(self, bb):
        # return the size of a bounding box
        if not type(bb) is self.BB:
            raise TypeError("bounding box required")
        return (bb.urp.x - bb.dlp.x) * (bb.urp.y - bb.dlp.x)

    def insert_list(self, lst):
        if type(lst) is not list and type(lst) is not set:
            raise TypeError('can only accept list')
        mp = dict()
        hilbert = HilbertCurve(128, 2)
        for point in lst:
            mp[point] = hilbert.distance_from_coordinates(point)

        reverse_hv_order = list()
        for k, v in sorted(mp.items(), key=lambda x: x[1], reverse=True):
            reverse_hv_order.append(k)

        for p in reverse_hv_order:
            self.insert(p[0], p[1])

    def insert(self, a, b):
        if type(a) is not int or type(b) is not int:
            raise TypeError('can only accept int, int')
        # insert procedure
        # a,b are two dimensions of a point
        p = self.Point(a, b)

        bb = self.genBB([p])

        if self.root is None:
            self.root = self.Node(self.degree)
            self.root.append(bb)

        else:
            res = self.recursive_insert(bb, self.root)
            if res is not None:
                l_node, r_node = res
                # create new root if split nodes returned
                bb0 = self.genBB(l_node.list_bb())
                bb1 = self.genBB(r_node.list_bb())
                n_node = self.Node(self.degree)
                n_node.append(bb0, l_node)
                n_node.append(bb1, r_node)
                self.root = n_node

    def recursive_insert(self, bb, n):
        # sub insert procedure
        # a,b are two dimensions of a point
        # can return split nodes or none
        if self.is_internal_node(n):
            for i, bb_n in enumerate(n.list_bb()):
                if self.is_completely_cover(bb, bb_n):
                    res = self.recursive_insert(bb, n.map[bb_n])
                    if res is not None:
                        return self.process_return_nodes(res[0], res[1], n, i)
                    return None

            # find the minimum bb in node has the smallest whose child node has the minim LHV
            minimum_lhv = sys.maxsize
            idx = None
            next_entry = None
            for i, bb_n in enumerate(n.list_bb()):
                # get the next entry
                entry = n.map[bb_n]
                if bb.hv < entry.LHV < minimum_lhv:
                    idx = i
                    minimum_lhv = entry.LHV
                    next_entry = entry

            resize_bb = self.genBB([bb, n.list_bb()[idx]])
            n.replace_with(idx, resize_bb)
            res = self.recursive_insert(bb, next_entry)
            if res is not None:
                return self.process_return_nodes(res[0], res[1], n, idx)
            return None

        else:
            if not n.append(bb):
                l_node, r_node = n.split()
                l_node.append(bb)
                return l_node, r_node

            return None

    def process_return_nodes(self, l_node, r_node, n, i):
        if not type(l_node) is self.Node or not type(r_node) is self.Node:
            raise TypeError('can only process type Node')

        # replace bb with return bbs if overhead split and return
        bb0 = self.genBB(l_node.list_bb())
        bb1 = self.genBB(r_node.list_bb())
        # delete old node
        n.remove(i)
        n.append(bb0, l_node)
        if not n.append(bb1, r_node):
            node0, node1 = n.split()
            node0.append(bb1, r_node)
            return node0, node1
        return None

    def over_lapped(self, bb0, bb1):
        # check of two bounding box has overlap
        if type(bb0) is not self.BB or type(bb1) is not self.BB:
            raise TypeError("can only compare bounding box")

        p0 = bb0.dlp
        p1 = bb0.urp

        g0 = bb1.dlp
        g1 = bb1.urp

        overlapped_dlp_x = max(p0.x, g0.x)
        overlapped_dlp_y = max(p0.y, g0.y)

        overlapped_urp_x = min(p1.x, g1.x)
        overlapped_urp_y = min(p1.y, g1.y)

        return overlapped_dlp_x <= overlapped_urp_x and overlapped_dlp_y <= overlapped_urp_y

    def is_point(self, bb):
        # decide whether bb is point or not
        if type(bb) is self.BB:
            return bb.urp.x == bb.dlp.x and bb.urp.y == bb.dlp.y
        if type(bb) is self.Point:
            return True

        return False

    def query_region(self, a, b, c, d):
        if a > c or b > d:
            raise ValueError("point0 must be on the down right of the point1")
        region = self.genBB([self.Point(a, b), self.Point(c, d)])
        return self.search_points_covered(self. root, region)

    def search_points_covered(self, n, region):
        # perform region query
        if type(n) is not self.Node:
            raise TypeError("only takes node as input")

        if type(region) is not self.BB:
            raise TypeError("only takes BB as input")

        if n is None:
            return list()
        ans = list()
        for re in n.list_bb():
            if self.over_lapped(re, region):
                if self.is_point(re):
                    ans.append(re)
                    continue
                if re in n.map:
                    lst = self.search_points_covered(n.map[re], region)
                    ans.extend(lst)

        return ans

    def cal_distance_euclidean(self, p0 , p1):
        # calculate the distance between 2 points
        if type(p0) is not self.Point or type(p1) is not self.Point:
            raise TypeError("can only calculate the distance between two points")
        return ((p0.x - p1.x)**2 + (p0.y - p1.y)**2)**0.5

    def get_min_max_dist_bb_to_p(self, bb, p):
        # get the min max distance of the bb related to point p
        if type(bb) is not self.BB or type(p) is not self.Point:
            raise TypeError("must take Bounding box and a Point as input")

        dist0 = self.cal_distance_euclidean(bb.urp, p)
        dist1 = self.cal_distance_euclidean(bb.dlp, p)

        dist2 = self.cal_distance_euclidean(self.Point(bb.dlp.x, bb.urp.y), p)
        dist3 = self.cal_distance_euclidean(self.Point(bb.urp.x, bb.dlp.y), p)

        maxdist = max(dist0, dist1, dist2, dist3)
        mindist = min(dist0, dist1, dist2, dist3)

        return mindist, maxdist

    def sort_box(self, node, p):
        if type(node) is not self.Node or type(p) is not self.Point:
            raise TypeError("can only take node as input")
        # sort boxes in nodes by its smallest dist to point p
        mp = dict()
        minimum_max = sys.maxsize
        for bb in node.list_bb():
            mp[bb] = self.get_min_max_dist_bb_to_p(bb, p)
            minimum_max = min(minimum_max, mp[bb][1])

        bbs = list()
        for bb, dists in sorted(mp.items(), key=lambda v: v[1]):
            bbs.append(bb)
        return bbs, mp

    def bounded_NN_search(self, a, b, c, d, x, y, exclude):
        # using euclidean distance
        # a search algorithm that finds the nearest point of the given point within the given range
        # a,b the down left coordinates of search area, c, d the up right coordinates of the search area.
        # x,y the coordinates of point whose NN(nearest neighbour) needs to be find.
        region = self.genBB([self.Point(a, b), self.Point(c, d)])
        point = self.Point(x, y)
        # recursive search use
        res = self.bounded_NN_search_helper(self.root, region, point, exclude)
        if res[0] is not None:
            return res[0].x, res[0].y
        return None

    def bounded_NN_search_helper(self, n, region, point, exclude):
        # n root
        # region: region to search
        # point: point whose NN needs to be find
        if type(n) is not self.Node or type(region) is not self.BB or type(point) is not self.Point:
            raise TypeError("can only take Node, BB, and Point as parameters")

        ans = None
        mdis = sys.maxsize

        if n is not None:
            bbs, mp = self.sort_box(n, point)
            for bb in bbs:
                # because boxes are sorted by its distance to point the remaining box can discard
                if mp[bb][0] > mdis:
                    break
                if self.over_lapped(bb, region):
                    if bb is not None and self.is_point(bb) and (bb.dlp.x, bb.dlp.y) not in exclude:
                        dis = self.cal_distance_euclidean(bb.dlp, point)
                        if dis < mdis:
                            mdis = dis
                            ans = bb.dlp
                    elif bb is not None and bb in n.map:
                        res_ans, res_dis = self.bounded_NN_search_helper(n.map[bb], region, point, exclude)
                        if res_ans is not None and res_dis is not None and res_dis < mdis:
                            mdis = res_dis
                            ans = res_ans
        return ans, mdis

