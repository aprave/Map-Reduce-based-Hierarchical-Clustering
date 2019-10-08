import random
import sys
import os
import math
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering

class Jaccard:
    def __init__(self):
        self.RANDOM_CONTENT_SIZE = 40
        self.COMMON_CONTENT_SIZE = 2000
        self.ROOT_FILE_NAME = ""
        self.COMMON_CONTENT = ""
        self.NUMBER_OF_FILES = 80
        self.file_fingerprint_dict={}

    def generate_file_fingerprint_map(self):

        for num in range(11,31):
           for k in range(1,5,1):
            print("file"+str(num)+ str(k)+".txt")
            self.file_fingerprint_dict.setdefault("file"+str(num)+ str(k)+".txt",'')
            f1 = open(os.getcwd() + "\\data\\file"+str(num)+ str(k)+".txt", "r", encoding='utf-8')
            fingerprints=[]
            contents=f1.read()
            x = contents[0: len(contents)-1].split(", ")
            for count in x:
                fingerprints.append(count)
            self.file_fingerprint_dict["file"+str(num)+ str(k)+".txt"] = fingerprints
        return self.file_fingerprint_dict

    def jaccard_similarity(self,list1,list2):
        intersection = len(list(set(list1).intersection(list2)))
        union = (len(list1) + len(list2)) - intersection
        # Produce the dissimilarity matrix
        return  1 - float(intersection / union)

    #get the jaccard similarity for all files

    def get_jaccard(self, dict):
        two_d=[]
        for i in range(11,31):
            for l in range(1,5,1):
                fp1 = dict["file"+str(i)+str(l)+".txt"]
                new=[]
                for j in range(11, 31):
                  for m in range(1,5,1):
                    fp2 = dict["file"+str(j)+str(m)+".txt"]
                    new.append(self.jaccard_similarity(fp1,fp2))
                two_d.append(new)
        return two_d



if __name__ == "__main__":
   dict=Jaccard().generate_file_fingerprint_map()
   signatures=Jaccard().get_jaccard(dict)
   X=np.array(signatures)
   cluster = AgglomerativeClustering(n_clusters=4, affinity='euclidean', linkage='ward')
   cluster.fit_predict(X)
   print(cluster.labels_)
   plt.scatter(X[:, 0], X[:, 1], c=cluster.labels_, cmap='rainbow')
   plt.show()
   for i in range(10):
        t = len(signatures[0])
        print(signatures[i])
        print("\n")
