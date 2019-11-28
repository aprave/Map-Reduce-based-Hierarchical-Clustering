package com.edu.cloud

import java.io.File


import org.apache.log4j.LogManager
import org.apache.spark.{SparkConf, SparkContext}

import scala.collection.mutable.ListBuffer
import scala.concurrent.forkjoin.ThreadLocalRandom

object Minhash2 {
  def main(args: Array[String]): Unit = {
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
    val FilesWithMinhash = sc.wholeTextFiles(args(0) + "/*.txt")
      .map(l => l._2).zipWithUniqueId().map(l => (l._2, l._1)).map(l =>(l._1, getMinhashedValue(l._2.split(","))))

  }

  def getMinhashedValue(fingerPrints : Array[String]) = {
    var nextPrime = 42949671L
    val ACoeff=new ListBuffer[Long]()
    val BCoeff=new ListBuffer[Long]()
    val random: ThreadLocalRandom = ThreadLocalRandom.current()

    for (i <- 1 to 50) {
      ACoeff+=random.nextLong(0, nextPrime)
      BCoeff+=random.nextLong(0, nextPrime)
    }
    var someData : Array[String] = new Array[String](50)
    for (i <- 0 to 49) {
      someData(i)  = fingerPrints.map(k => ((ACoeff(i) * k.replaceAll("\\s", "").toInt + BCoeff(i)) % nextPrime)).min.toString()
    }
    someData
  }


}
