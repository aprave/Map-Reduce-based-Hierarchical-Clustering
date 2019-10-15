import random
import sys
import os
import math
import numpy as py  
class Jaccard:
    def __init__(self):
        self.file_fingerprint_dict={}
    #generate file fingerprint map
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

    # jaccard similarity formula
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
    # def getSmallestDissimilarity(self, signature) :
    #     min = sys.maxsize
    #     minIndex = ()
        
    #     for i in range(0, len(signatures)):
    #         for j in range(0, len(signatures[0])) :
    #             if signature[i][j] > 0 and signature[i][j] < min :
    #                 min = signature[i][j]
    #                 minIndex = (i, j)
    #     return (min, minIndex)

               
        
# if __name__ == "__main__":
#     dict1 = Jaccard().generate_file_fingerprint_map()
#     cluster_history = []
#     signatures = Jaccard().get_jaccard(dict1)
#     for i in range(10):
#         t = len(signatures[0])
#         ClusterSet().initializeClusterSet(signatures[0])
#         print("\n")
    #create a map of maps
    # cluster_history.append(closest(1))


    
    
