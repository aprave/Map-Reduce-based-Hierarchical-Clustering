import random
import sys
import os

maxSysNumber = 2 ** 32 - 1
nextPrime = 4294967311
class Minhash:
    def __init__(self):
        self.RANDOM_CONTENT_SIZE = 40
        self.COMMON_CONTENT_SIZE = 2000
        self.ROOT_FILE_NAME = ""
        self.COMMON_CONTENT = ""
        self.NUMBER_OF_FILES = 20
        self.file_fingerprint_dict={}
        self.coeffA = []
        self.coeffB = []

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

    def get_min_hashes(self, dict):
        self.coeffA = self.pickRandomCoeffs(10)
        self.coeffB = self.pickRandomCoeffs(10)
        signatures=[]
        for num in range(self.NUMBER_OF_FILES):
                fingerprintIDs = dict["file"+str(num)+".txt"]
                signature = []
                for i in range(10):
                    minHashCode = nextPrime + 1
                    for fingerprint in fingerprintIDs:
                        if fingerprint != '':
                            hashCode = (self.coeffA[i] * int(fingerprint) + int(self.coeffB[i])) % nextPrime
                            if hashCode < minHashCode:
                                minHashCode = hashCode
                    signature.append(minHashCode)
                signatures.append(signature)
        return signatures




if __name__ == "__main__":
   dict=Minhash().generate_file_fingerprint_map()
   signatures=Minhash().get_min_hashes(dict)
   print(signatures)
