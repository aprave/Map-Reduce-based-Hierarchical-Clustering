import random
import sys
import os
import time
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering

maxSysNumber = 2 ** 32 - 1
nextPrime = 4294967311
class Minhash:
    def __init__(self):
        self.RANDOM_CONTENT_SIZE = 40
        self.COMMON_CONTENT_SIZE = 2000
        self.ROOT_FILE_NAME = ""
        self.COMMON_CONTENT = ""
        self.NUMBER_OF_FILES = 200
        self.file_fingerprint_dict={}
        self.coeffA = []
        self.coeffB = []

    def getTriangleIndex(self,i, j):
        if i == j:
            sys.stderr.write("Can't access triangle matrix with i == j")
            sys.exit(1)
        if j < i:
            temp = i
            i = j
            j = temp
        k = int(i * (200 - (i + 1) / 2.0) + j - i) - 1

        return k
    def pickRandomCoeffs(self, k):
        randList = []
        while k > 0:
            randIndex = random.randint(0, maxSysNumber)
            while randIndex in randList:
                randIndex = random.randint(0, maxSysNumber)
            randList.append(randIndex)
            k = k - 1
        return randList

    def generate_file_fingerprint_map(self):

        for num in range(11, 31):
           for k in range(1, 5, 1):
            self.file_fingerprint_dict.setdefault("file"+str(num)+ str(k)+".txt",'')
            f1 = open(os.getcwd() + "\\data\\file"+str(num)+ str(k)+".txt", "r", encoding='utf-8')
            fingerprints=[]
            contents=f1.read()
            x = contents[0: len(contents)-1].split(", ")
            for count in x:
                fingerprints.append(count)
            self.file_fingerprint_dict["file"+str(num)+ str(k)+".txt"] = fingerprints
        return self.file_fingerprint_dict

    def get_min_hashes(self, dict):
        self.coeffA = self.pickRandomCoeffs(50)
        self.coeffB = self.pickRandomCoeffs(50)
        signatures=[]
        t0 = time.time()
        new_dict={}
        for num in range(11, 31):
            for k in range(1, 5, 1):
                fingerprintIDs = dict["file"+str(num)+ str(k)+".txt"]
                signature = []
                new_dict.setdefault("file"+str(num)+ str(k)+".txt","")
                for i in range(50):
                    minHashCode = nextPrime + 1
                    for fingerprint in fingerprintIDs:
                        if fingerprint != '':
                            hashCode = (self.coeffA[i] * int(fingerprint) + int(self.coeffB[i])) % nextPrime
                            if hashCode < minHashCode:
                                minHashCode = hashCode
                    signature.append(minHashCode)
                signatures.append(signature)
                new_dict["file"+str(num)+ str(k)+".txt"]=signature
        elapsed = (time.time() - t0)
        return signatures, new_dict

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

    def jaccard_similarity(self,list1,list2):
        intersection = len(list(set(list1).intersection(list(set(list2)))))
        union = (len(list1) + len(list2)) - intersection
        return float(intersection / union)

    #get the jaccard similarity for all files

    def get_minhash_estimation(self, dict):
        two_d=[]
        for count, i in enumerate(dict, 0):
                fp1 = dict[i]
                new=[]
                for count,j in enumerate(dict,0):
                    fp2 = dict[j]
                    new.append(self.jaccard_similarity(fp1,fp2))
                two_d.append(new)
        return two_d



if __name__ == "__main__":
   dict=Minhash().generate_file_fingerprint_map()
   signatures,new_dict = Minhash().get_min_hashes(dict)
   min_estimation = Minhash().get_minhash_estimation(new_dict)
   jaccard = Minhash().get_jaccard(dict)
   diff=np.array(jaccard)-np.array(min_estimation)
   print(np.std(diff))