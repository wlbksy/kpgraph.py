import numpy as np
import scipy.sparse as sp
import pickle

id_raw =[]
with open('adj.list','r') as f:
    for line in f.readlines():
        line = line[:-1]
        ids = list(set([int(id) for id in line.split(',')]))
        id_raw.append(ids)

with open('adj.self','r') as f:
    for line in f.readlines():
        line = line[:-1]
        ids = [int(line)]
        id_raw.append(ids)


id_list = list(set([j for i in id_raw for j in i]))

id_len = len(id_list)

adjM = np.zeros(shape=(id_len, id_len), dtype=np.int)

for line in id_raw:
    line_len = len(line)
    for i in range(line_len):
        i_idx = id_list.index(line[i])
        if line_len==1:
            adjM[i_idx, i_idx] += 1
        for j in range(i+1, line_len):
            j_idx = id_list.index(line[j])
            adjM[i_idx, j_idx] += 1
            adjM[j_idx, i_idx] += 1

adjMatCSR = sp.csr_matrix(adjM)
pickle.dump(adjMatCSR, open('adjMatCSR.pickle','wb'))
pickle.dump(id_list, open('id_list.pickle','wb'))
