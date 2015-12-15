# -*- coding:utf-8 -*-
import numpy as np
import scipy.sparse as sp
import pickle
import networkx as nx

# id_list = ['a','b','c','d','e','f','g','h']

demo_arr = np.array([
            [0,40,0,0,0,0,0,0],
            [0,0,0,10,0,100,20,0],
            [0,0,0,0,0,0,0,0],
            [0,0,1,0,5,0,0,0],
            [0,0,0,200,0,0,0,0],
            [0,0,0,0,100,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,3],
            ])

adjMatCSR = sp.csr_matrix(demo_arr)
invWeightMat = sp.csr_matrix((1/adjMatCSR.data, adjMatCSR.nonzero()))
# pickle.dump(invWeightMat, open('graph.pickle', 'wb'))

g = nx.from_scipy_sparse_matrix(invWeightMat, create_using=nx.DiGraph())

class student:
    def __init__(self, start, goals):
        all_path_dict = dict()
        newgoals = goals
        newgoals.insert(0, start)
        # newgoals = [start, *goals]
        len_goals = len(newgoals)
        for i in range(len_goals-1):
            tmp_path_dict = dict()
            for j in range(i+1, len_goals):
                try:
                    tmp_path_dict[newgoals[j]] = nx.shortest_path(g, source=newgoals[i], target=newgoals[j], weight='weight')
                except:
                    tmp_path_dict[newgoals[j]] = []
            all_path_dict[newgoals[i]] = tmp_path_dict
        # print(all_path_dict)

        self.mastered_nodes = [] # 实际学习路径
        self.route_nodes = [] # 最优学习路径
        self.fail_register = []

        for tgt in range(len_goals):
            tgt_path = False
            for src in range(tgt):
                src_path = all_path_dict[newgoals[src]]
                src_tgt_path = src_path[newgoals[tgt]]
                for node in src_tgt_path:
                    if node not in self.route_nodes:
                        self.route_nodes.append(node)
                    tgt_path = True
            if not tgt_path:
                self.route_nodes.append(newgoals[tgt])

    def next(self, this, master_bool):
        if master_bool: # 掌握this，前往next
            self.fail_register = []
            if this not in self.mastered_nodes:
                self.mastered_nodes.append(this)

            return self.checkInSequence(this)

        else:
            thisCol = invWeightMat[:, this]
            thisPrevID = thisCol.nonzero()[0].tolist()

            if this in self.fail_register:
                self.fail_register.append(this)
                if len(self.fail_register) >= 3:
                    for i in thisPrevID:
                        try:
                            self.mastered_nodes.remove(i)
                        except:
                            pass
                    return self.checkInSequence(this)
            else:
                self.fail_register = [this]

            # 未掌握this，前往其它this前驱
            thisPrevData = dict(zip(thisPrevID, thisCol.data))

            while True:
                thisPrevID = list(thisPrevData.keys())
                if (not thisPrevID) or (thisPrevID==[this]): # 没有其它this前驱
                    return this
                else:
                    if this in thisPrevData:
                        del thisPrevData[this]
                    nextID = min(thisPrevData, key=thisPrevData.get)
                    if nextID in self.mastered_nodes:
                        del thisPrevData[nextID]
                    else:
                        return nextID

    def checkInSequence(self, this):
        # 按顺序检查节点
        untouched_nodes = set(self.route_nodes) - set(self.mastered_nodes)
        if untouched_nodes:
            untouched_nodes_index = [self.route_nodes.index(i) for i in untouched_nodes]
            return self.route_nodes[min(untouched_nodes_index)]
        else:
            return "Done!"

    def getRealPath(self):
        return self.mastered_nodes
    def getIdealPath(self):
        return self.route_nodes
