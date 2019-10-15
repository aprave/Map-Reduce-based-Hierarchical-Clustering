import random
import sys
import os
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from Cluster import Cluster


# 32 bit number limit and prime number
maxSysNumber = 2 ** 32 - 1
nextPrime = 4294967311

# class to calculate Minhash Estimation of Jaccard Similarity


class Minhash:
    def __init__(self):
        self.file_fingerprint_dict = {}
        self.coeffA = []
        self.coeffB = []

    # pick random coefficients  a and b for hash function ax+b%c
    def pickRandomCoeffs(self, k):
        randList = []
        while k > 0:
            randIndex = random.randint(0, maxSysNumber)
            while randIndex in randList:
                randIndex = random.randint(0, maxSysNumber)
            randList.append(randIndex)
            k = k - 1
        return randList

    # generate file fingerprint map
    def generate_file_fingerprint_map(self):

        for num in range(11, 31):
            for k in range(1, 5, 1):
                self.file_fingerprint_dict.setdefault(
                    "file"+str(num) + str(k)+".txt", '')
                f1 = open(os.getcwd() + "\\data\\file"+str(num) +
                          str(k)+".txt", "r", encoding='utf-8')
                fingerprints = []
                contents = f1.read()
                x = contents[0: len(contents)-1].split(", ")
                for count in x:
                    fingerprints.append(count)
                self.file_fingerprint_dict["file" +
                                           str(num) + str(k)+".txt"] = fingerprints
        return self.file_fingerprint_dict

    def get_min_hashes(self, dict):
        self.coeffA = self.pickRandomCoeffs(50)
        self.coeffB = self.pickRandomCoeffs(50)
        signatures = []
        t0 = time.time()
        new_dict = {}
        for num in range(11, 31):
            for k in range(1, 5, 1):
                fingerprintIDs = dict["file"+str(num) + str(k)+".txt"]
                signature = []
                new_dict.setdefault("file"+str(num) + str(k)+".txt", "")
                for i in range(50):
                    minHashCode = nextPrime + 1
                    for fingerprint in fingerprintIDs:
                        if fingerprint != '':
                            hashCode = (
                                self.coeffA[i] * int(fingerprint) + int(self.coeffB[i])) % nextPrime
                            if hashCode < minHashCode:
                                minHashCode = hashCode
                    signature.append(minHashCode)
                signatures.append(signature)
                new_dict["file"+str(num) + str(k)+".txt"] = signature
        elapsed = (time.time() - t0)
        return signatures, new_dict

    # get jaccard similarity
    def get_jaccard(self, dict):
        two_d = []
        for i in range(11, 31):
            for l in range(1, 5, 1):
                fp1 = dict["file"+str(i)+str(l)+".txt"]
                new = []
                for j in range(11, 31):
                    for m in range(1, 5, 1):
                        fp2 = dict["file"+str(j)+str(m)+".txt"]
                        new.append(self.jaccard_similarity(fp1, fp2))
                two_d.append(new)
        return two_d

    # jaccard similarity formula
    def jaccard_similarity(self, list1, list2):
        intersection = len(list(set(list1).intersection(list(set(list2)))))
        union = (len(list1) + len(list2)) - intersection
        return 1 - float(intersection / union)

    # get jaccard similarity values for the min hashes calculated in the dict
    def get_minhash_estimation(self, clusterSet):
        count = 0
        for c in clusterSet:
            for d in clusterSet:
                if c.clusterId == d.clusterId:
                    c.jaccards[d.clusterId] = 0
                    count = count + 1
                else:
                    c.jaccards[d.clusterId] = self.jaccard_similarity(
                        c.getMinhash(), d.getMinhash())


    # get jaccard and minhash estimation of jaccard and compute standard deviation
if __name__ == "__main__":
    dict = Minhash().generate_file_fingerprint_map()
    signatures, new_dict = Minhash().get_min_hashes(dict)
    min_estimation = Minhash().get_minhash_estimation(new_dict)
    jaccard = Minhash().get_jaccard(dict)
    diff_list = []
    sum = 0
    for i in range(80):
        new_list = []
        x = jaccard[i]
        y = min_estimation[i]
        for count, k in enumerate(x, 0):
            z = k-y[count]
            new_list.append(z*z)
            sum += z*z
        diff_list.append(new_list)
    SD = math.sqrt(sum/80)
    print("Standard Deviation >>>>>>  " + str(SD))
