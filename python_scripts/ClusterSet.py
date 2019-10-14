from Cluster import Cluster
from jaccard import Jaccard
import sys
from min_hash_estimation import Minhash


class ClusterSet:
    clusters = []

    def addCluster(self, cluster):
        self.clusters.append(cluster)

    def initializeClusterSet(self, minHashDict):
        for key in minHashDict.keys():
            c = Cluster(key)
            c.addMinhashes(minHashDict[key])
            self.clusters.append(c)

    def getClusters(self):
        return self.clusters

    def computeMinhashEstimation(self):
        Minhash().get_minhash_estimation(self.getClusters())

    def getClosestClusters(self):
        closest = ()
        minimumDistance = sys.maxsize
        for c in self.clusters:
            for d in self.clusters:
                if c.jaccards[d.clusterId] < minimumDistance and c.clusterId != d.clusterId:
                    closest = (c, d)
                    minimumDistance = c.jaccards[d.clusterId]
        return (closest, minimumDistance)

    def clusterMinSets(self, minClusters):
        mergedCluster = Cluster(
            minClusters[0].clusterId + minClusters[1].clusterId)
        mergedCluster.minHashes = list(set().union(
            minClusters[0].minHashes, minClusters[1].minHashes))
        updatedClusterSet = list(filter(
            lambda x: x.clusterId != minClusters[0].clusterId and x.clusterId != minClusters[1].clusterId, self.clusters))
        for c in updatedClusterSet:
            newJaccard = Minhash().jaccard_similarity(
                mergedCluster.minHashes, c.minHashes)
            mergedCluster.jaccards[c.clusterId] = newJaccard
            c.jaccards[mergedCluster.clusterId] = newJaccard
            c.jaccards.pop(minClusters[0].clusterId, None)
            c.jaccards.pop(minClusters[1].clusterId, None)
        updatedClusterSet.append(mergedCluster)
        self.clusters = updatedClusterSet
       # mergedCluster.jaccards = setJaccards(mergedCluster, minClusters)
        # updatedClusters = list(filter(lambda x: x.clusterId != minClusters(
        #     0).id or x.clusterId != minClusters(1).id))

        # def getSmallestJaccardValue(self):
        #     for c in clusters:

        # def mergeClusters(self, c1, c2):
        #     total = c1.signatures.union(c2.signatures)
        #     c = Cluster()
        #     c.addSignature(total)
        #     clusters.removeCluster(c1);
        #     clusters.removeCluster(c2);
        #     clusters.addCluster(c);
