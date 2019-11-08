package com.edu.cloud

import scala.collection.mutable.ListBuffer


class ClusterSet(c:ListBuffer[Cluster]) {
    var clusters: ListBuffer[Cluster] = c
    var key: Int = 0
    def addCluster(c: Cluster): Unit = {
        clusters += c
    }

    def getClusters(): ListBuffer[Cluster] = {
        return clusters
    }

    def getLastKey() : Int = {
    return key;
    }
    def setLastKey(lastKey : Int): Unit = {
        key = lastKey
    }
    def computeMinhashEstimation(): Unit = {
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

    def clusterMinSets(minClusters: (ListBuffer[Cluster], Double)): Unit = {
        val newKey = getLastKey()
        val fingerPrint: List[Long] = List.concat(minClusters._1(0).fingerPrint, minClusters._1(1).fingerPrint) //merge fingerprints
        val jac= Map[Int, Double]()
        val mergedHashes :List[Long] = minClusters._1(0).minHash.toSet.union(minClusters._1(1).minHash.toSet).toList    //merge minHash

        //Create a new cluster with these variables
        var mergedCluster = new Cluster(newKey,fingerPrint ,jac , mergedHashes)
        setLastKey(newKey + 1)
        var updatedClusterSet = new ListBuffer[Cluster]()
        for (x<-clusters){
            if(x.clusterId != minClusters._1(0).clusterId && x.clusterId != minClusters._1(1).clusterId){
                updatedClusterSet += x
            }
        }
        updatedClusterSet += mergedCluster
        println(updatedClusterSet , updatedClusterSet.length)
        for(c <-updatedClusterSet){
            var newJaccard : Double = MinHash.jaccard_similarity(mergedCluster.minHash.toSet, c.minHash.toSet)
            mergedCluster.jaccard+=c.clusterId-> newJaccard
            c.jaccard+=mergedCluster.clusterId-> newJaccard
            c.jaccard -= minClusters._1(0).clusterId
            c.jaccard -= minClusters._1(1).clusterId
        }
        clusters = updatedClusterSet
    }
}