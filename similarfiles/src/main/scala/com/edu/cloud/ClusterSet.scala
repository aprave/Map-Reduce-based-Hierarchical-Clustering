package com.edu.cloud

import scala.collection.mutable.ListBuffer


class ClusterSet(c:ListBuffer[Cluster]){
    var clusters = c
    def addCluster(c : Cluster): Unit = {
        clusters+=c
    }
    def getClusters() :  ListBuffer[Cluster] ={
        return clusters
    }
}
    def computeMinhashEstimation() = {
        var d = new ClusterSet(clusters)
        MinHash.get_minhash_estimation(d)
    }
    /* Calculates closest cluster and returns the distance */

    def getClosestClusters(): (ListBuffer[Cluster], Double) = {
        val clusterSet = new ClusterSet(clusters)
        var closest = ListBuffer[Cluster]()
        var minimumDistance = Double.MaxValue
        for (c <- clusterSet.getClusters()) {
            for (d <- clusterSet.getClusters()) {
                if(c.jaccard.contains(d.clusterId)) {
                    val dist = c.jaccard(d.clusterId)
                    if(dist<minimumDistance & c.clusterId!=d.clusterId ){
                        closest += (c,d)
                        minimumDistance = dist
                    }
                }
            }
        }
     return (closest, minimumDistance)
    }
}
