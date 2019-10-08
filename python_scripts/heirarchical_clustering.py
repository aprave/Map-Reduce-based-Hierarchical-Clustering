import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

from sklearn.cluster import AgglomerativeClustering
fingerprints = {}
for i in range(0,11) :
    fileName =os.getcwd() + "\\data\\file" + str(i) + ".txt"
    print(fileName)
    f = open(fileName, "r")
    for line in f.readlines():
      if i in fingerprints :
          fingerprints[i].append(line);
      else :
          fingerprints[i] = [line]
    f.close();
print(fingerprints)
# x = np.array([[5,3],
#     [10,15],
#     [15,12],
#     [24,10],
#     [30,30],
#     [85,70],
#     [71,80],
#     [60,78],
#     [70,55],
#     [80,91],])
# cluster = AgglomerativeClustering(n_clusters=2, affinity='jaccard', linkage='average')
# cluster.fit_predict(x)
# print("entered inside the script")
# plt.scatter(x[:,0],x[:,1], c=cluster.labels_, cmap='rainbow')
# plt.show()


