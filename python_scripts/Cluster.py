class Cluster:
    jaccards = {}
    minHashes = []
    clusterId = ""
    def __init__(self, clusterId) :
        self.clusterId = clusterId
    def addMinhashes(self, minHashes):
        self.minHashes = minHashes
    def getMinhash(self):
        return self.minHashes
    

        
        
