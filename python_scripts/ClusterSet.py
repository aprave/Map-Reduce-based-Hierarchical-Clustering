from Cluster import Cluster
from jaccard import Jaccard
class ClusterSet:
    clusters = []
    jaccardMatrix = []
    def addCluster(self, cluster):
        self.clusters.append(cluster)
    def initializeClusterSet(self) :
        dict1 = Jaccard().generate_file_fingerprint_map()
        cluster_history = []
        signatures = Jaccard().get_jaccard(dict1)
        for i in range(10):
            c  = Cluster()
            c.addSignature(signatures[i])
            ClusterSet.addCluster(self, c)
        return ClusterSet
    def getClusters(self) :
        return self.clusters
    def mergeClusters(self, c1, c2):
        total = c1.signatures.union(c2.signatures)
        c = Cluster()
        c.addSignature(total)
        clusters.removeCluster(c1);
        clusters.removeCluster(c2);
        clusters.addCluster(c);
