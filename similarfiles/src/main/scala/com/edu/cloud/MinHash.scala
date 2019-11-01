package com.edu.cloud

import org.apache.log4j.LogManager
import org.apache.log4j.Level
import org.apache.spark.{SparkConf, SparkContext}
import java.io.File

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
    val files = getListOfFiles(new File(args(0)), okFileExtensions)
    val random: ThreadLocalRandom = ThreadLocalRandom.current()
    //files.foreach(println)
    var nextPrime = 4294967311L
    val ACoeff=new ListBuffer[Long]()
    val BCoeff=new ListBuffer[Long]()
    for (i <- 1 to 50) {
      val coeffA = sc.parallelize(Seq[Int](), 1)
        .mapPartitions { _ => {
          (1 to 1).map { _ => random.nextLong(0, nextPrime) }.iterator
        }
        }
      val arr=coeffA.collect()
      for(j<-arr){
        ACoeff+=j
      }
      val coeffB = sc.parallelize(Seq[Int](), 1)
        .mapPartitions { _ => {
          (1 to 1).map { _ => random.nextLong(0, nextPrime) }.iterator
        }
        }
      val arr1 = coeffB.collect()
      for(j<- arr1)
      {
        BCoeff+=j
      }
    }
    var fileFingerprintMap = scala.collection.mutable.Map[String, List[Long]]()
    for(filePath <- files){
      //println(filePath)
      val textFile = sc.textFile(filePath)
      var fingerPrintVal = new ListBuffer[String]()
      val result = textFile.flatMap(line => line.split(","))
      result.collect().foreach(fingerPrintVal+=_.trim())
      val fingerprints= fingerPrintVal.toList
      val fileName=filePath.slice(filePath.lastIndexOf("\\")+1,filePath.length())
      var fValues=new ListBuffer[Long]
      for (i<-fingerprints)
          fValues+=i.toLong
      println(fileName)
      fileFingerprintMap+=(fileName->fValues.toList)
      for(fingerprint <- fingerprints){
        //println(fingerprint)
      }
      //println("res="+result.collect())
      //result.saveAsTextFile(args(1))
    }
    println("map size"+fileFingerprintMap.size)
    val fileSignatureMap = scala.collection.mutable.Map[String, List[Long]]()
    for ((fileName,fingerPrints) <- fileFingerprintMap) {
      //println("NIRUPP"+fileName)
      val min=0
      var fileSignatures = new ListBuffer[Long]()
      for (i <- 0 to 49) {
        var minHashCode = nextPrime + 1
        for(k<-fingerPrints) {
          val hashCode = (ACoeff(i) *k + BCoeff(i)) % nextPrime
          if(hashCode<minHashCode)
            minHashCode = hashCode
        }
        fileSignatures+=minHashCode
      }
      fileSignatureMap +=(fileName -> fileSignatures.toList)
    }
    var convertToList = new ListBuffer[String]()
    for ((fileName,fingerPrints) <- fileSignatureMap) {
      convertToList+=fileName+","+fingerPrints
    }
    val signatureMap=sc.parallelize(convertToList)
    signatureMap.saveAsTextFile("output")
  }

  def getListOfFiles(dir: File, extensions: List[String]): List[String] = {
    dir.listFiles.filter(_.isFile).toList.filter { file =>
      extensions.exists(file.getName.endsWith(_))
    }.map(_.getPath)
  }
}


