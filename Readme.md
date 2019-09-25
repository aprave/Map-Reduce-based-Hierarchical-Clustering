** **

## Using map-reduce based hierarchical clustering to find similar files in a large dataset

## 1.   Vision and Goals Of The Project:

The current demands for datacenters is huge and storing backups can become a tedious task. Moving massive data in the production environment is both computationally and spatially expensive, to tackle this Dell's DDFS (Data Domain File System) provides deduplication that splits files into chunks. Hierarchical clustering would allow us to iteratively predict similarity in files with more confidence. Scaling our solution using map-reduce also enables us to perform deduplication on a multi-node distributed system.

Our short term goal in this project is to develop a clustering algorithm that can potentially find similar files on a single node. Our efforts would be focused on finding techniques that can predict similarity in files, starting at minhash estimation of the Jaccard distance and further support linkage algorithms such as max/complete linkage, average linkage. We plan to extend this solution to a multi-node distributed system using map-reduce, allowing us to process larger datasets. 

The goal of the project:
* Develop a clustering algorithm that is scalable w.r.t. memory requirement.

## 2. Users/Personas Of The Project:
Researchers working on DDFS (Data Domain File System by Dell)

## 3.   Scope and Features Of The Project:

The main features we are aiming to implement were elucidated by our mentor:

* Create python programs that can implement a basic clustering algorithm for the datasets on a single node
* Report findings on which algorithm is more suitable on the basis of data set size i.e. min-hash estimation of the Jaccard distance, max/complete linkage, average linkage.
* Extend this solution to develop programs that can run on multiple nodes to solve the clustering algorithm (using map reduce) and   produce an end result that looks like:

           	Cluster#  	  |  Dissimilarity Level |	File ID’s

** **

## 4. Solution Concept
The below system diagram shows how files from DDFS are processed to find simliar files using fingerprint computation, jaccard index calculation and parallelized hierarchical clustering.
<img src="/images/workflow.png" width="800" height="600">
* Fingerprint Computation: A fingerprinting algorithm is a procedure that maps an arbitrarily large data item (such as a computer file) to a much shorter bit string, its fingerprint, that uniquely identifies the original data for all practical purposes. Fingerprints are typically used to avoid the comparison and transmission of bulky data. For instance, a web browser or proxy server can efficiently check whether a remote file has been modified, by fetching only its fingerprint and comparing it with that of the previously fetched copy. In our project we will be computing fingerprints of a dataset of 100K-100TB file sizes for 100M-1B files.
<img src="/images/Fingerprint.svg.png" width="400" height="300">

* Deduplication-Data deduplication is a technique for eliminating duplicate copies of repeating data. A related and somewhat synonymous term is single-instance (data) storage. This technique is used to improve storage utilization and can also be applied to network data transfers to reduce the number of bytes that must be sent. In the deduplication process, unique chunks of data, or byte patterns, are identified and stored during a process of analysis. In our project we will be globalizing deduplication by locating all similar files in the same node.

* Distance Matrix Computation: Computation of the distance matrix can be expensive. Most algorithms use approximation to update the matrix. The size of the matrix is O(n^2) and we can run out of memory quickly. 
* Hierarchical Clustering: Our objects are files. DDFS has already chunked them into 8-12K chunks, each of which is represented by a SHA1 fingerprint (20 + 4 bytes). Similarity between 2 files is measured by the Jaccard index
J(A, B) = |A ∩ B| / |A U B|
The distance would be 1 – J(A, B). We want to identify clusters of similar files. Most clustering algorithm takes a distance matrix and just combine the most similar files 2 at a time (or some variations)

* Minhash- Check locality sensitive hashing.
Minhash for a file-Apply a uniformly distributed hash function to the fingerprints in a file. Hash function maps keys to numbers, thus providing an order. Minhash is the smallest hash number for the file. Yes – we represent a file by only one number. If two files have Jaccard Index J(A, B), the probability that they have the same minhash is J(A, B). Now generate n hash functions, compute the minhash for each function. We now have a minhash signature of n numbers
Given the minhash signature of 2 files, #same entries/#total entries = J(A, B)
Given the minhash signature of A and B, {a1,a2,a3,… an} and {b1, b2, b3, … bn}  the minhash of the union A U B is
{min(a1,b1), min(a2,b2), … min(an, bn)}
If we know |A| and |B| and J(A, B), we can estimate
           |A U B| and |A ∩ B|




## 5. Acceptance criteria

The minimum acceptance criteria for the project is as follows :
* Develop a  clustering algorithm that finds similar files on a single node using min hashing estimation of Jaccard indices.
* Report possible solutions for a scaled-out architecture of the clustering algorithm that performs clustering on multiple nodes using map-reduce.
Stretch goals:
* Compare the following approaches for finding the distance between files:
 * Max/complete linkage 
 * Average linkage.
 * Min-hash estimation of the Jaccard Index

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

References :
https://pdfs.semanticscholar.org/7b12/f6ef8d620bcc54e71da13df4291bcc8d0679.pdf
** **
