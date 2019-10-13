from ClusterSet import ClusterSet

cs = ClusterSet()
cs.initializeClusterSet();
clusters = cs.getClusters()
for i in range(0, len(clusters)):
    print(clusters[i].signatures)
