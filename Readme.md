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

The Scope places a boundary around the solution by detailing the range of features and functions of the project. This section helps to clarify the solution scope and can explicitly state what will not be delivered as well.

It should be specific enough that you can determine that e.g. feature A is in-scope, while feature B is out-of-scope.

** **

## 4. Solution Concept

This section provides a high-level outline of the solution.

Global Architectural Structure Of the Project:

This section provides a high-level architecture or a conceptual diagram showing the scope of the solution. If wireframes or visuals have already been done, this section could also be used to show how the intended solution will look. This section also provides a walkthrough explanation of the architectural structure.

 

Design Implications and Discussion:

This section discusses the implications and reasons of the design decisions made during the global architecture design.

## 5. Acceptance criteria

This section discusses the minimum acceptance criteria at the end of the project and stretch goals.

## 6.  Release Planning:

Release planning section describes how the project will deliver incremental sets of features and functions in a series of releases to completion. Identification of user stories associated with iterations that will ease/guide sprint planning sessions is encouraged. Higher level details for the first iteration is expected.

** **

## General comments

Remember that you can always add features at the end of the semester, but you can't go back in time and gain back time you spent on features that you couldn't complete.
