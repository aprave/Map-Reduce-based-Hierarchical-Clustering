class Cluster:
    jaccards = {}
    minHashes = []
    clusterId = ""
    clusterName = ""

    def __init__(self, clusterId):
        self.clusterId = clusterId

    def addMinhashes(self, minHashes):
        self.minHashes = minHashes

    def addName(self, name):
        self.clusterName = name

    def getMinhash(self):
        return self.minHashes
