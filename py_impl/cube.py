#%%
import sys
import numpy as np
from itertools import combinations

cube_verts = np.array([
    [1,1,1],
    [-1,1,1],
    [1,-1,1],
    [1,1,-1],
    [-1,-1,1],
    [1,-1,-1],
    [-1,1,-1],
    [-1,-1,-1]
])

cube_edges = np.array([
    [1,1,0],
    [1,0,1],
    [0,1,1],
    [1,-1,0],
    [1,0,-1],
    [0,1,-1],
    [-1,1,0],
    [-1,0,1],
    [0,-1,1],
    [-1,-1,0],
    [-1,0,-1],
    [0,-1,-1]
])

cube_faces = np.array([
    [1,0,0],
    [0,1,0],
    [0,0,1],
    [-1,0,0],
    [0,-1,0],
    [0,0,-1],
])

subgroups = []

rotx = np.array([[1,0,0],[0,0,-1],[0,1,0]])
roty = np.array([[0,0,1],[0,1,0],[-1,0,0]])
rotz = np.array([[0,-1,0],[1,0,0],[0,0,1]])

m_x = np.array([[-1,0,0],[0,1,0],[0,0,1]])
m_y = np.array([[1,0,0],[0,-1,0],[0,0,1]])
m_z = np.array([[1,0,0],[0,1,0],[0,0,-1]])

cube = np.vstack((cube_faces, cube_verts, cube_edges))

test = cube

vert_len = test.shape[0]
mask = np.zeros(vert_len,dtype=bool)

def encode(trusses):
    enc = ['0'] * vert_len
    for t in trusses:
        i_f = np.where((test == t).all(1))[0]
        if (i_f.shape[0] != 0): #6 bits
            enc[i_f[0]] = '1'
    return int("".join(enc),2)

def decode(e):
    mask = np.zeros(vert_len, dtype=bool)
    nummask = [bit == '1' for bit in bin(e)[2:]]
    mask[vert_len-len(nummask):] = nummask
    return test[mask]

# complete = set(range(2**vert_len))
truss_elem_num = int(sys.argv[1])
complete = set((2**np.array(list(combinations(range(vert_len), truss_elem_num)))).sum(1))
print("Length of complete set: ",len(complete))

type_classes = []

while complete:
    e = complete.pop()
    tr = decode(e)
    tmp = set()
    tmp.add(e)
    if e == 0:
        complete -= tmp
        type_classes.append(tmp)
        continue
    tmp.add(encode((m_z@tr.T).T))
    for rot in [rotx, rotx, rotz, rotx, rotx, rotz]:
        for j in range(4):
            tr = (roty@tr.T).T
            tmp.add(encode(tr))
            tmp.add(encode((m_z@tr.T).T))
        tr = (rot@tr.T).T
        # tmp.add(encode(tr))
        # tmp.add(encode((m_z@tr.T).T))

    complete -= tmp
    type_classes.append(tmp)

# TODO: listing each truss separately
for i,cl in enumerate(type_classes):
    r = next(iter(cl))
    i_f = 0
    i_e = 0
    i_v = 0
    trusses = decode(r)
    # for t in trusses:
    #     if 
    print(i,":", decode(r),"\tlength: ", len(cl))
# print(type_classes)
print(len(type_classes), " number of distinct configurations for ", truss_elem_num, " number of truss elements")

connected = 0
for cl in type_classes:
    r = next(iter(cl))
    edges = decode(r)
    fill_vol = np.zeros((3,3,3), dtype=int)
    fill_vol[1,1,1] = 1
    indices = np.nonzero(fill_vol)
    prev_fill = np.copy(fill_vol)
    while(True):
        for x, y, z in zip(*np.nonzero(fill_vol)):
            for e in edges:
                fill_vol[(e[0]+x) % 3,(e[1]+y) % 3,(e[2]+z) % 3] = 1
        if (prev_fill == fill_vol).all():
            break
        prev_fill = np.copy(fill_vol)
    if (fill_vol == 1).all():
        # print("Representative ", r, ": \n\n", edges, "\nis fully connected\n")
        connected += 1

print("Total ", connected, " fully connected representatives")
        


# for i in range(2**vert_len):
#     sg = []
#     mask[:] = 0
#     nummask = [bit == '1' for bit in bin(i)[2:]]
#     mask[vert_len-len(nummask):] = nummask
#     points = test[mask]
#     sg.append(points)
#     if points.shape[0] == 0:
#         continue
#     points = (m_z@points.T).T
#     sg.append(points)
#     for rot in [rotx, rotx, rotz, rotx, rotx, rotz]:
#         for j in range(4):
#             points = (roty@points.T).T
#             sg.append(points)
#             sg.append((m_z@points.T).T)
#             points = (rot@points.T).T

#     uniq_sg = True
#     gindex = 0
#     for gi, g in enumerate(subgroups):
#         if g[0].shape[0] != sg[0].shape[0]:
#             continue
#         for e_1 in g:
#             for e_2 in sg:
#                 if (e_1==e_2).all():
#                     uniq_sg = False
#                     gindex = gi
#                     break
#             if not uniq_sg:
#                 break
#         if not uniq_sg:
#             break
    
#     if uniq_sg:
#         subgroups.append(sg)
#         print("#sg: ",len(subgroups), "\t i: ", i/2**vert_len)
#     # else:
#     #     subgroups[gindex].extend(sg)

    
# print(len(subgroups))

# for sg in subgroups:
    # print(sg[0])

# for g in subgroups:
#     print(g[0])


    


            


    



