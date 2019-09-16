** **

## Using map-reduce based hierarchical clustering to find similar files in a large dataset

## 1.   Vision and Goals Of The Project:

The vision of the project is to find clusters of similar files among massive datasets. It is really difficult to find similarity between two files that are huge in size. The problem becomes more complicated when the number of files that are needed to be analyzed is also huge in numbers and it is required to find the clusters of similar files. 
Hierarchical clustering is one of the prominent and widely-used data mining techniques for its informative representation of clustering results.
In the face of the ever-growing datasets, the single-machine performance of hierarchical clustering algorithm can no longer keep up the game, which creates an urgent demand for a parallel solution. However, the parallelization of hierarchical clustering algorithm is a non-trivial task. 
This project will research upon approaches to parallelize hierarchical clustering by using map reduce technique which is an efficient way to implement parallelization. Most clustering algorithm takes a distance matrix and just combine the most similar files two at a time (or some variation), But this computation can be expensive. 

The steps below outline the high level goals that will be a part of this project : 
* Create a scaled-out architecture – a cluster with many nodes.
* Currently deduplication occurs within a single node but we are required to implement deduplication  globally by locating all similar files in the same node.
* Create a  clustering algorithm that can be scaled to many nodes.
* Find similar files using clustering algorithms in massive large datasets.
* Optimize the clustering by computing hierarchical clusters for subset of files and then assign the remaining files in the top down manner.
* Further optimization by considering a subset of fingerprints or some minhash of the fingerprints rather than all the fingerprints.
* To find out how good is sampling approach as compared to non-sampling approach.

## 2. Users/Personas Of The Project:

Anyone who is handling file systems in an organization are the end users of the project.
* Cloud admin users.
* The scaled out clustering algorithm will be used within the global dedupe engine of DDFS.
* File System Administrators of file systems.
* Advanced users with complex requirements who are expected to use storage systems


** **

## 3.   Scope and Features Of The Project:

* To use fingerprints associated with each file to analyze the jaccard similarity.
* Compute minhash of all files in a massive dataset.
* Use Jaccard similarity index to compute the similarity among files in the dataset.
* Perform hierarchical clustering using the similarity index.
* Scalability: Can scale to large number of files, projects, and services.


** **

## 4. Solution Concept

* Fingerprint Computation: A fingerprinting algorithm is a procedure that maps an arbitrarily large data item (such as a computer file) to a much shorter bit string, its fingerprint, that uniquely identifies the original data for all practical purposes. Fingerprints are typically used to avoid the comparison and transmission of bulky data. For instance, a web browser or proxy server can efficiently check whether a remote file has been modified, by fetching only its fingerprint and comparing it with that of the previously fetched copy. In our project we will be computing fingerprints of a dataset of 100K-100TB file sizes for 100M-1B files.
<img src="/images/Fingerprint.svg.png" width="400" height="300">

* Deduplication-Data deduplication is a technique for eliminating duplicate copies of repeating data. A related and somewhat synonymous term is single-instance (data) storage. This technique is used to improve storage utilization and can also be applied to network data transfers to reduce the number of bytes that must be sent. In the deduplication process, unique chunks of data, or byte patterns, are identified and stored during a process of analysis. In our project we will be globalizing deduplication by locating all similar files in the same node.

* Distance Matrix Computation: Computation of the distance matrix can be expensive. Most algorithms use approximation to update the matrix. The size of the matrix is O(n^2) and we can run out of memory quickly. 
* Hierarchical Clustering: Our objects are files. DDFS has already chunked them into 8-12K chunks, each of which is represented by a SHA1 fingerprint (20 + 4 bytes). Similarity between 2 files is measured by the Jaccard index
J(A, B) = |A ∩ B| / |A U B|
The distance would be 1 – J(A, B). We want to identify clusters of similar files. Most clustering algorithm takes a distance matrix and just combine the most similar files 2 at a time (or some variations)

* Minhash- Check locality sensitive hashing
Minhash for a file-Apply a uniformly distributed hash function to the fingerprints in a file. Hash function maps keys to numbers, thus providing an order. Minhash is the smallest hash number for the file. Yes – we represent a file by only one number. If two files have Jaccard Index J(A, B), the probability that they have the same minhash is J(A, B). Now generate n hash functions, compute the minhash for each function. We now have a minhash signature of n numbers
Given the minhash signature of 2 files, #same entries/#total entries = J(A, B)
Given the minhash signature of A and B, {a1,a2,a3,… an} and {b1, b2, b3, … bn}  the minhash of the union A U B is
{min(a1,b1), min(a2,b2), … min(an, bn)}
If we know |A| and |B| and J(A, B), we can estimate
           |A U B| and |A ∩ B|




## 5. Acceptance criteria

The minimum acceptance criteria for this project is to research upon various approaches to find an algorithm that can find the similarity among files using jaccard indexing as the distance matrix and be able to classify files into groups of clusters. Once the algorithm is obtained, research on finding solutions to decrease the space complexity of the program and improve its performance.

## 6.  Release Planning:

Release #1 (due by Week 2): 
File Data Set Generation  : For this project, files contain 32 or 64 bit random numbers – each represents a chunk of data.

For example, file A = { 1203, 402392, 2300, 23, 102393822, …. }
             file B = { 32393000, 103032923, 29393, 123002, 123, 2300, … }
             
We need to create files with similar data. There are a few “canonical” building blocks:
* Files that are unique
* Chain of files with p% common data between adjacent files:
F1, F2, F3, … such that Fi and Fj share p% of common data
* A binary hierarchy relationship like this:
<img src="/images/Tree.PNG" width="300" height="300">
* Minhash Signature : Generate min hashes for the files created above.

Release # 2 : (due by week 4)
Accuracy of minhash estimates : Once the files have been generated, run some clustering algorithm to combine the files based on similarity.

Release # 3 : 
Improve the efficiency of the clustering algorithm by improving the space efficiency.
.

** **

## General comments

Remember that you can always add features at the end of the semester, but you can't go back in time and gain back time you spent on features that you couldn't complete.
