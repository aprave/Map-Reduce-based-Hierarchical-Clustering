** **

## Using map-reduce based hierarchical clustering to find similar files in a large dataset

## 1.   Vision and Goals Of The Project:

The current demands for datacenters are huge and storing backups can become a tedious task. Moving massive data in the production environment is both computationally and spatially expensive. To resolve this, Dell's DDFS (Data Domain File System) provides deduplication that splits files into chunks. Using Hierarchical clustering would allow us to iteratively predict similarity in files with more confidence. Scaling our solution using map-reduce also enables us to perform deduplication on a multi-node distributed system.

Our short term goal in this project is to develop a clustering algorithm that can potentially find similar files on a single node. Our efforts would be focused on finding techniques that can predict similarity in files, starting at minhash estimation of the Jaccard distance and further support linkage algorithms such as max/complete linkage, average linkage. We plan to extend this solution to a multi-node distributed system using map-reduce, allowing us to process larger datasets. 

The goal of the project:
* Report performance related findings on various file similarity calculation algorithms.
* Develop a clustering algorithm that is scalable w.r.t. memory requirement.

## 2. Users/Personas Of The Project:
Researchers working on DDFS (Data Domain File System by Dell)

## 3.   Scope and Features Of The Project:

The main features we are aiming to implement were elucidated by our mentor:

* Create python programs that can implement a basic clustering algorithm for the datasets on a single node
* Report findings on various file similarity calculation algorithms( min-hash, Jaccard index, max/complete linkage, average linkage) based on their performance for different parameters like dataset size.
* Extend this solution to develop programs that can run on multiple nodes to solve the clustering algorithm (using map reduce) and   produce an end result that looks like:

           	ClusterID  |  Dissimilarity Level  |   File IDs

** **

## 4. Solution Concept
_Overview_

<img src="/images/mapreduce.PNG" width="750" height="1000">

_Fig 1- The workflow diagram of the project. The first step is to generate dataset files with fingerprints. The second step is to get initial dissimilarity matrix. This matrix is input to first iteration of map reduce and the output of first map reduce iteration is input to the second iteration and so on until the optimal solution is reached._

* Fingerprint Computation: A fingerprinting algorithm is a procedure that maps an arbitrarily large data item (such as a computer file) to a much shorter bit string, its fingerprint, that uniquely identifies the original data for all practical purposes. Fingerprints are typically used to avoid the comparison and transmission of bulky data. For instance, a web browser or proxy server can efficiently check whether a remote file has been modified, by fetching only its fingerprint and comparing it with that of the previously fetched copy. In our project we will be computing fingerprints of a dataset of 100K-100TB file sizes for 100M-1B files. We are generating our dataset files by using random 32-64 bit integers as fingerprints and by keeping a certain percentage of similar fingerprints in some of the dataset files.
<img src="/images/Fingerprint.svg.png" width="400" height="300">

* Deduplication-Data deduplication is a technique for eliminating duplicate copies of repeating data. A related and somewhat synonymous term is single-instance (data) storage. This technique is used to improve storage utilization and can also be applied to network data transfers to reduce the number of bytes that must be sent. In the deduplication process, unique chunks of data, or byte patterns, are identified and stored during a process of analysis. In our project we will be globalizing deduplication by locating all similar files in the same node.

* Distance Matrix Computation: Similarity between two files is measured by the Jaccard index J(A, B) = |A ∩ B| / |A U B|. The distance would be 1 – J(A, B). We want to identify clusters of similar files. Most clustering algorithm takes a distance matrix and just combine the most similar files two at a time (or some variations). Computation of the distance matrix can be expensive. Most algorithms use approximation to update the matrix. The size of the matrix is O(n^2) and we can run out of memory quickly.

* Minhash- Check locality sensitive hashing.
Minhash for a file-Apply a uniformly distributed hash function to the fingerprints in a file. Hash function maps keys to numbers, thus providing an order. Minhash is the smallest hash number for the file. Yes – we represent a file by only one number. If two files have Jaccard Index J(A, B), the probability that they have the same minhash is J(A, B). Now generate n hash functions, compute the minhash for each function. We now have a minhash signature of n numbers
Given the minhash signature of 2 files, #same entries/#total entries = J(A, B)
Given the minhash signature of A and B, {a1,a2,a3,… an} and {b1, b2, b3, … bn}  the minhash of the union A U B is
{min(a1,b1), min(a2,b2), … min(an, bn)}
If we know |A| and |B| and J(A, B), we can estimate
           |A U B| and |A ∩ B|
 * Hierarchical clustering - It is one of the popular and easy to understand clustering technique.
For this project, initially each data point is considered as an individual cluster. At each iteration, similar clusters will merge with other clusters until one cluster or K clusters are formed.The basic algorithm is :  
          
   * Compute the proximity matrix  
   * Let each data point be a cluster  
   * Repeat: Merge the two closest clusters and update the proximity matrix until there is no change in the matrix.  
   * Since hierarchical clustering needs to create a distance matrix in order to compute similarities it proves to be highly space  inefficient especially when number of files are large. However, if the algorithm is scaled and distributed across multiple nodes, it can highly improve performance. In order to accomplish this, the project will use map reduce to process the distance matrix over multiple nodes.
           
 * Finding Similarities among files - Apart from calculating Jaccard index, the following measures can be used to find distance between two hash functions :  
 **single linkage algorithm** : can be defined as the similarity of two clusters C1 and C2 is equal to the minimum of the similarity between points Pi and Pj such that Pi belongs to C1 and Pj belongs to C2.  
Sim(C1,C2) = Min Sim(Pi,Pj) such that Pi ∈ C1 & Pj ∈ C2  
**complete linkage algorithm** : this is exactly opposite to the MIN approach. The similarity of two clusters C1 and C2 is equal to the maximum of the similarity between points Pi and Pj such that Pi belongs to C1 and Pj belongs to C2.  
Sim(C1,C2) = Max Sim(Pi,Pj) such that Pi ∈ C1 & Pj ∈ C2  
**Group Average** : Take all the pairs of points and compute their similarities and calculate the average of the similarities.  
Mathematically this can be written as,  
sim(C1,C2) = ∑ sim(Pi, Pj)/|C1|*|C2|  





## 5. Acceptance criteria

*The minimum acceptance criteria for the project is as follows :*

* Develop a  clustering algorithm that finds similar files on a single node using min hashing estimation of Jaccard indices.
* Report possible solutions for a scaled-out architecture of the clustering algorithm that performs clustering on multiple nodes using map-reduce.

*Stretch goals:*
* Compare the following approaches for finding the distance between files:

     * Max/complete linkage 
     * Average linkage.
     * Min-hash estimation of the Jaccard Index

## 6.  Release Planning:

Release #1 (due by Week 2): 

File Data Set Generation  : For this project, files contain 32 or 64 bit integers – each represents a chunk of data.

For example, file A = { 1203, 402392, 2300, 23, 102393822, …. }
             file B = { 32393000, 103032923, 29393, 123002, 123, 2300, … }
             
We need to create files with similar data. There are a few “canonical” building blocks:
* Files that are unique
* Chain of files with p% common data between adjacent files:
F1, F2, F3, … such that Fi and Fj share p% of common data
* A binary hierarchy relationship like this:
<img src="/images/Hierarchy.PNG" width="300" height="300">

Minhash Signature : Generate min hashes for the files created above.

Release # 2 (due by week 4)

* Minhash estimation of the Jaccard distance

Release # 3 : (due by week 6)

* A basic clustering algorithm that supports minhashing.

Release # 4 : (due by week 8)

* Implement iterate map reduce clustering algorithm

Release # 5 : (due by week 10)

* Report the efficiency improvement experiments of the clustering algorithm by improving the space efficiency.

Release # 6 : (due by week 12)

_Stretch Goals:_
Iterative clustering algorithm that supports following linkage algorithms:
* Max/Complete linkage
* Average linkage

## Open Questions?
* Apart from researchers at Dell Data Domain File System team, who else will be the users and personas for this project?

* How do we design the dissimilarity matrix and are there any ways to alter the representation so as to reduce the spatial complexity?

## Presentations:
Demo 1:
https://docs.google.com/presentation/d/1QKXyxbTsCa_3MybXeT2vbhxHfIkL4UOI8EqA_8rBoV8/edit?usp=sharing

References :
https://pdfs.semanticscholar.org/7b12/f6ef8d620bcc54e71da13df4291bcc8d0679.pdf
** **
