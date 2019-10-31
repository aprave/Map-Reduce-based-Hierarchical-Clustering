from ClusterSet import ClusterSet
from min_hash_estimation import Minhash

cs = ClusterSet()
dict = Minhash().generate_file_fingerprint_map()
signatures, new_dict = Minhash().get_min_hashes(dict)
# adds all minhashes to cluster set and creates clusters
cs.initializeClusterSet(new_dict)
cs.computeMinhashEstimation()  # initalizes the minhashes
# compute jaccard values for every cluster

# jaccard = Minhash().get_jaccard(dict)

clusters = cs.getClusters()
while len(clusters) > 1:
    minCluster = cs.getClosestClusters()
    cs.clusterMinSets(minCluster[0])
    clusters = cs.getClusters()
    print("Clusters Left : " + str(len(clusters)))
    # print(minCluster[0][0].clusterId, minCluster[0][1].clusterId)
