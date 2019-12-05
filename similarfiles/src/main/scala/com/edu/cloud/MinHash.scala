package com.edu.cloud

import org.apache.log4j.LogManager

import org.apache.log4j.Level
import org.apache.spark.{ SparkConf, SparkContext }
import java.io.File
import org.apache.spark.rdd.RDD

import org.apache.spark.SparkConf

import scala.collection.mutable.ListBuffer
import scala.concurrent.forkjoin.ThreadLocalRandom
import scala.util.Random

//With Scala you might now want to use Amazon's official SDK for Java which provides the AmazonS3::listObjects method:

import scala.collection.JavaConverters._
import scala.collection.mutable
import com.amazonaws.services.s3.model.ObjectListing
import org.apache.hadoop.fs.FileSystem
import java.net.URI
import org.apache.hadoop.fs.Path
import org.apache.hadoop.fs.LocatedFileStatus
import util.control.Breaks._

object MinHash {
  def main(args: Array[String]) {
    print("Hello")
    val logger: org.apache.log4j.Logger = LogManager.getRootLogger
    if (args.length != 2) {
      logger.error("Usage:\nmain.MinHash <input dir> <output dir>")
      System.exit(1)
    }
    println(args(0))
    println(args(1))
    var isLocal = false
    if(!args(0).contains("s3:")){
      isLocal = true
    }
    val conf = new SparkConf().setAppName("MinHash")
    /**
     * Important: To run on AWS comment the line above and uncomment the line below
     	 val conf = new SparkConf().setAppName("MinHash")   
     *
     **/
    if(isLocal){
      conf.setMaster("local[*]")
    }
    
    
    
    //conf.set("spark.hadoop.validateOutputSpecs", "false");

      val sc = new SparkContext(conf)

    //load textfile into spark
    val okFileExtensions = List("txt")
    val random: ThreadLocalRandom = ThreadLocalRandom.current()
    //files.foreach(println)
    var nextPrime = 42949671L
    val ACoeff = new ListBuffer[Long]()
    val BCoeff = new ListBuffer[Long]()
    for (i <- 1 to 50) {
      ACoeff += random.nextLong(0, nextPrime)
      BCoeff += random.nextLong(0, nextPrime)
    }
    var resultRDD = sc.emptyRDD[Long]
    val fileSignatureMap = scala.collection.mutable.Map[String, List[Long]]()
    sc.broadcast(ACoeff)
    sc.broadcast(BCoeff)
    
    /**
     * Important: To run on AWS comment the line above and uncomment the line below
     */
    //for(filePath <- getListOfFiles(okFileExtensions, sc)){
    var filePaths = List[String]()
    if(isLocal){
      filePaths = getLocalListOfFiles(new File(args(0)), okFileExtensions)
    }else{
      filePaths = getListOfFiles(args(0), okFileExtensions, sc)
    }
    for(filePath <- filePaths){
      //create rdd
      var fingerPrints = sc.textFile(filePath)
        .flatMap(line => line.split(","))
        .map(fp => fp.trim().toLong)
      var fingerPrintsRdd = fingerPrints.cache()
      val min = 0
      var fileSignatures = new ListBuffer[Long]()
      for (i <- 0 to 49) {
        var fingerPrintsRdd = fingerPrints
        var minHashCode = nextPrime + 1
        fileSignatures += fingerPrintsRdd.map(k => ((ACoeff(i) * k + BCoeff(i)) % nextPrime)).min()
      }
      fileSignatureMap += ((filePath.slice(filePath.lastIndexOf("\\") + 1, filePath.length())) -> fileSignatures.toList)
    }
//    var filesMinHashPairRdd = sc.parallelize(fileSignatureMap.toSeq)
//      val result = filesMinHashPairRdd.cartesian(filesMinHashPairRdd).map {
//      case (t1: (String, List[Long]), t2: (String, List[Long])) if t1 != t2 => (t1._1, t2._1, jaccard_similarity(t1._2.toSet, t2._2.toSet))
//    }
//    filesMinHashPairRdd.saveAsTextFile(args(1))
    println("completed reading")
    println("fileSignatureMap size =" + fileSignatureMap.size)
    
    var convertToList = new ListBuffer[String]()
    for ((fileName, fingerPrints) <- fileSignatureMap) {
      convertToList += fileName + "," + fingerPrints
    }
    val signatureMap = sc.parallelize(convertToList)
    val clusterSet = new ClusterSet(new ListBuffer[Cluster]())

    for ((k, v) <- fileSignatureMap) {
      println("key is ")

      var key = clusterSet.getLastKey()
      println(key)
      val cluster = new Cluster(key, List[Long](), Map[Int, Double](), v)
      clusterSet.addCluster(cluster)
      clusterSet.setLastKey(key + 1)
    }
    get_minhash_estimation(clusterSet)
    for (c <- clusterSet.getClusters()) {
      println("cluster id is ")
      println(c.clusterId)
      println(c.jaccard)
    }
    val minCluster: (ListBuffer[Cluster], Double) = clusterSet.getClosestClusters()
    println(clusterSet.getClosestClusters()._1(0).clusterId)
    println(clusterSet.getClosestClusters()._1(1).clusterId)
    println("Jaccard of 0", clusterSet.getClosestClusters()._1(0).jaccard)
    println("Jaccard of 1", clusterSet.getClosestClusters()._1(1).jaccard)

    var h = new Hierarchical(clusterSet)
    h.performHierarchical()
    //    signatureMap.saveAsTextFile("output")
  }

  def jaccard_similarity(l1: Set[Long], l2: Set[Long]): Double = {
    val unified: Set[Long] = l1.union(l2);
    val intersection: Set[Long] = l1.intersect(l2);
    return intersection.size.toFloat / unified.size
  }
  def get_minhash_estimation(clusterSet: ClusterSet): Unit = {
    var count = 0
    for (c <- clusterSet.getClusters()) {
      for (d <- clusterSet.getClusters()) {
        if (c.clusterId == d.clusterId) {
          c.jaccard += (d.clusterId -> 0)
          count = count + 1
        } else {
          c.jaccard += (d.clusterId -> jaccard_similarity(c.minHash.toSet, d.minHash.toSet))
        }
      }
    }
  }
  
  def getLocalListOfFiles(dir: File, extensions: List[String]): List[String] = {
    dir.listFiles.filter(_.isFile).toList.filter { file =>
      extensions.exists(file.getName.endsWith(_))
    }.map(_.getPath)
  }

  def getListOfFiles(path: String, extensions: List[String], sc: SparkContext): List[String] = {
    val MAX_FILES = 500
    val fs = FileSystem.get(URI.create(path), sc.hadoopConfiguration)

    val it = fs.listFiles(new Path(path), true)
    val validFiles = mutable.ListBuffer.empty[String]
    breakable {
      while (it.hasNext()) {
        val nextFile = it.next();
        println("next file:" + nextFile.getPath.getName)
        if (nextFile.isFile() && extensions.exists(nextFile.getPath.getName.endsWith(_))) {

          if (validFiles.size <= MAX_FILES) {
            validFiles += nextFile.getPath.toString()
            println("Adding file path: " + nextFile.getPath)
          } else {
            break
          }
        }
      }
    }
    println("Total files read  : " + validFiles.size)
    return validFiles.toList
  }

}