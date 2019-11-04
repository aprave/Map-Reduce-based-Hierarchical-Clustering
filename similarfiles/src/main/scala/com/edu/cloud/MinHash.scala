package com.edu.cloud

import org.apache.log4j.LogManager
import org.apache.log4j.Level
import org.apache.spark.{SparkConf, SparkContext}
import java.io.File
import org.apache.spark.rdd.RDD

import org.apache.spark.SparkConf

import scala.collection.mutable.ListBuffer
import scala.concurrent.forkjoin.ThreadLocalRandom
import scala.util.Random

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
    val conf = new SparkConf().setAppName("MinHash").setMaster("local[*]")
    //conf.set("spark.hadoop.validateOutputSpecs", "false");
    val sc = new SparkContext(conf)
    //load textfile into spark
    val okFileExtensions = List("txt")
    //create rdd
    val files = sc.parallelize(getListOfFiles(new File(args(0)), okFileExtensions))
    val random: ThreadLocalRandom = ThreadLocalRandom.current()
    //files.foreach(println)
    var nextPrime = 4294967311L
    val ACoeff=new ListBuffer[Long]()
    val BCoeff=new ListBuffer[Long]()
    for (i <- 1 to 50) {
      ACoeff+=random.nextLong(0, nextPrime)
      BCoeff+=random.nextLong(0, nextPrime)
    }
    
    var resultRDD = sc.emptyRDD[Long]
    
    val fileSignatureMap = scala.collection.mutable.Map[String, List[Long]]()
    //var resultRDD = sc.emptyRDD[Long]
    var fileList = files.collect()
    sc.broadcast(ACoeff)
    sc.broadcast(BCoeff)
    for (filePath <- fileList) {
        var fingerPrints = sc.textFile(filePath)
            .flatMap(line => line.split(","))
            .map(fp => fp.trim().toLong)
        var fingerPrintsRdd =fingerPrints.cache()   
        val min = 0
        var fileSignatures = new ListBuffer[Long]()
        for (i <- 0 to 49) {
            var fingerPrintsRdd =fingerPrints
            var minHashCode = nextPrime + 1
            fileSignatures += fingerPrintsRdd.map(k => ((ACoeff(i) * k + BCoeff(i)) % nextPrime)).min()
        }
        fileSignatureMap +=((filePath.slice(filePath.lastIndexOf("\\")+1,filePath.length())) -> fileSignatures.toList)
    }
    println("completed reading")
    var convertToList = new ListBuffer[String]()
    for ((fileName,fingerPrints) <- fileSignatureMap) {
      convertToList+=fileName+","+fingerPrints
    }
    val signatureMap=sc.parallelize(convertToList)
    signatureMap.saveAsTextFile("output")
  }
  
    //# jaccard similarity formula
  def jaccard_similarity(list1: List[Long], list2: List[Long]): Float = {
      var intersection = ((list1.toSet).intersect(list2.toSet)).size
      var union = ((list1).size + (list2).size) - intersection
        return 1 - (intersection.toFloat/ union)
  }
  
  /*def get_minhash_estimation(clusterSet :ClusterSet){
     var count = 0
     for(c <- clusterSet){
         for(d <- clusterSet){
                if(c.clusterId == d.clusterId){
                    c.jaccards[d.clusterId] = 0
                    count = count + 1
                }else{
                    c.jaccards[d.clusterId] = jaccard_similarity(c.getMinhash(), d.getMinhash())
               }
         }
      }
  }*/
  

  

  

  def getListOfFiles(dir: File, extensions: List[String]): List[String] = {
    dir.listFiles.filter(_.isFile).toList.filter { file =>
      extensions.exists(file.getName.endsWith(_))
    }.map(_.getPath)
  }
  
}