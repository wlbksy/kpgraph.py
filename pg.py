import numpy as np
import scipy.sparse as sp
import pickle

# import matplotlib.pyplot as plt

adjMat_csc = pickle.load(open('adjMat_csc.pickle','rb'))
id_list = pickle.load(open('id_list.pickle','rb'))


print(len(id_list))


def normOutdegree(mat):
    outdegreeM = mat.sum(axis=1).repeat(mat.shape[0], axis=1)
    probilityM = mat/outdegreeM
    probilityM[np.isnan(probilityM)] = 0
    return probilityM

