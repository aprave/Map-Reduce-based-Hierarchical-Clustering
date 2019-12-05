

package com.edu.cloud

class Cluster(id: Int, fingerPrints: List[Long], jaccards: Map[Int, Double], minHashes: List[Long]) {
  var clusterId : Int = id;
  var fingerPrint: List[Long] = fingerPrints;
  var jaccard : Map[Int, Double] = jaccards
  var minHash : List[Long] = minHashes

  def getFingerPrint(): List[Long] = {
    return fingerPrint;
  }


  def setJaccard(j : Map[Int, Double]) = {
      jaccard = j;
  }
}


