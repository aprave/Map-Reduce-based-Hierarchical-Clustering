import random
import sys
import os
import math

class Jaccard:
    def __init__(self):
        self.RANDOM_CONTENT_SIZE = 40
        self.COMMON_CONTENT_SIZE = 2000
        self.ROOT_FILE_NAME = ""
        self.COMMON_CONTENT = ""
        self.NUMBER_OF_FILES = 20
        self.file_fingerprint_dict={}

    def generate_file_fingerprint_map(self):

        for num in range(self.NUMBER_OF_FILES):
            self.file_fingerprint_dict.setdefault("file"+str(num)+".txt",'')
            f1 = open(os.getcwd() + "\\data\\file"+ str(num)+".txt", "r", encoding='utf-8')
            fingerprints=[]
            contents=f1.read()
            x = contents[0: len(contents)-1].split(", ")
            for count in x:
                fingerprints.append(count)
            self.file_fingerprint_dict["file"+str(num)+".txt"] = fingerprints
        return self.file_fingerprint_dict

    def jaccard_similarity(self,list1,list2):
        intersection = len(list(set(list1).intersection(list2)))
        union = (len(list1) + len(list2)) - intersection
        return float(intersection / union)

    #get the jaccard similarity for all files

    def get_jaccard(self, dict):
        two_d=[]
        for i in range(self.NUMBER_OF_FILES):
                fp1 = dict["file"+str(i)+".txt"]
                new=[]
                for j in range(self.NUMBER_OF_FILES):
                    fp2 = dict["file"+str(j)+".txt"]
                    new.append(self.jaccard_similarity(fp1,fp2))
                two_d.append(new)
        return two_d



if __name__ == "__main__":
   dict=Jaccard().generate_file_fingerprint_map()
   signatures=Jaccard().get_jaccard(dict)
   print(signatures)
