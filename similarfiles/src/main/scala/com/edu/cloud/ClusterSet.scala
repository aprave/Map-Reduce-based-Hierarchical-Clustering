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