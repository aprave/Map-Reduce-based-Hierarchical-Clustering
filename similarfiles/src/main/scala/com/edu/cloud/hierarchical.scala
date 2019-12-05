package com.edu.cloud

import scala.collection.mutable.ListBuffer

//Given a clusterSet, return the output of hierarchical clustering

class Hierarchical(cluster: ClusterSet) {
  var cs : ClusterSet = cluster;
  def performHierarchical() {
    var clusters: ListBuffer[Cluster] = cs.getClusters()
    while (clusters.length > 1) {
      val minCluster = cs.getClosestClusters()
      cs.clusterMinSets(minCluster)
      clusters = cs.getClusters()
      println(clusters.length)
      println("Clusters Left: ", clusters.length)
      print(minCluster._1(0).clusterId, minCluster._1(1).clusterId)
    }
  }

}
