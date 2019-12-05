# Makefile for Clustering project.

# Customize these paths for your environment.
# -----------------------------------------------------------
spark.root=/users/sanketsaurav/software/spark-2.3.1-bin-without-hadoop
hadoop.root=/Users/sanketsaurav/software/hadoop-2.9.1
app.name=MinHash
jar.name=similarfiles.jar
maven.jar.name=similarfiles-1.0.jar
job.name=com.edu.cloud.MinHash
local.master=local[4]
# local.input=/Users/sanketsaurav/git/cs6220/Using_map-reduce_based_hierarchical_clustering_to_find_similar_files_in_a_large_datas/python_scripts/dataset
local.input=input
local.output=output
# Pseudo-Cluster Execution
hdfs.user.name=joe
hdfs.input=input
hdfs.output=output
# AWS EMR Execution
aws.jobtitle=SimFile-500-2m-2x-large-run-2	
aws.subnet.id=subnet-d86ee8bf
aws.emr.release=emr-5.17.0
aws.bucket.name=cs6240-mr-bucket
aws.input=similar-file-large-input
aws.output=output/${aws.jobtitle}
aws.log.dir=log/${aws.jobtitle}
aws.num.nodes=2		
aws.instance.type=m4.2xlarge
# -----------------------------------------------------------

# Compiles code and builds jar (with dependencies).
jar:
	mvn clean package
	cp target/${maven.jar.name} ${jar.name}

# Removes local output directory.
clean-local-output:
	rm -rf ${local.output}*

# Runs standalone
local: jar clean-local-output
	spark-submit --class ${job.name} --master ${local.master} --name "${app.name}" ${jar.name} ${local.input} ${local.output}

# Start HDFS
start-hdfs:
	${hadoop.root}/sbin/start-dfs.sh

# Stop HDFS
stop-hdfs: 
	${hadoop.root}/sbin/stop-dfs.sh
	
# Start YARN
start-yarn: stop-yarn
	${hadoop.root}/sbin/start-yarn.sh

# Stop YARN
stop-yarn:
	${hadoop.root}/sbin/stop-yarn.sh

# Reformats & initializes HDFS.
format-hdfs: stop-hdfs
	rm -rf /tmp/hadoop*
	${hadoop.root}/bin/hdfs namenode -format

# Initializes user & input directories of HDFS.	
init-hdfs: start-hdfs
	${hadoop.root}/bin/hdfs dfs -rm -r -f /user
	${hadoop.root}/bin/hdfs dfs -mkdir /user
	${hadoop.root}/bin/hdfs dfs -mkdir /user/${hdfs.user.name}
	${hadoop.root}/bin/hdfs dfs -mkdir /user/${hdfs.user.name}/${hdfs.input}

# Load data to HDFS
upload-input-hdfs: start-hdfs
	${hadoop.root}/bin/hdfs dfs -put ${local.input}/* /user/${hdfs.user.name}/${hdfs.input}

# Removes hdfs output directory.
clean-hdfs-output:
	${hadoop.root}/bin/hdfs dfs -rm -r -f ${hdfs.output}*

# Download output from HDFS to local.
download-output-hdfs:
	mkdir ${local.output}
	${hadoop.root}/bin/hdfs dfs -get ${hdfs.output}/* ${local.output}

# Runs pseudo-clustered (ALL). ONLY RUN THIS ONCE, THEN USE: make pseudoq
# Make sure Hadoop  is set up (in /etc/hadoop files) for pseudo-clustered operation (not standalone).
# https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/SingleCluster.html#Pseudo-Distributed_Operation
pseudo: jar stop-yarn format-hdfs init-hdfs upload-input-hdfs start-yarn clean-local-output 
	spark-submit --class ${job.name} --master yarn --deploy-mode cluster ${jar.name} ${local.input} ${local.output}
	make download-output-hdfs

# Runs pseudo-clustered (quickie).
pseudoq: jar clean-local-output clean-hdfs-output 
	spark-submit --class ${job.name} --master yarn --deploy-mode cluster ${jar.name} ${local.input} ${local.output}
	make download-output-hdfs

# Create S3 bucket.
make-bucket:
	aws s3 mb s3://${aws.bucket.name}

# Upload data to S3 input dir.
upload-input-aws: make-bucket
	aws s3 sync ${local.input} s3://${aws.bucket.name}/${aws.input}
	
# Delete S3 output dir.
delete-output-aws:
	aws s3 rm s3://${aws.bucket.name}/ --recursive --exclude "*" --include "${aws.output}*"

# Upload application to S3 bucket.
upload-app-aws:
	aws s3 cp ${jar.name} s3://${aws.bucket.name}

# Main EMR launch.
aws: jar upload-app-aws delete-output-aws
	aws emr create-cluster \
		--name "SimFile Spark Cluster Large Demo" \
		--release-label ${aws.emr.release} \
		--instance-groups '[{"InstanceCount":${aws.num.nodes},"InstanceGroupType":"CORE","InstanceType":"${aws.instance.type}"},{"InstanceCount":1,"InstanceGroupType":"MASTER","InstanceType":"${aws.instance.type}"}]' \
	    --applications Name=Hadoop Name=Spark \
		--steps Type=CUSTOM_JAR,Name="${app.name}",Jar="command-runner.jar",ActionOnFailure=TERMINATE_CLUSTER,Args=["spark-submit","--deploy-mode","cluster","--class","${job.name}","s3://${aws.bucket.name}/${jar.name}","s3://${aws.bucket.name}/${aws.input}","s3://${aws.bucket.name}/${aws.output}"] \
		--log-uri s3://${aws.bucket.name}/${aws.log.dir} \
		--use-default-roles \
		--enable-debugging \
		--auto-terminate \
		--ec2-attributes SubnetId=${aws.subnet.id}
		
# Download output from S3.
download-output-aws: clean-local-output
	mkdir ${local.output}
	aws s3 sync s3://${aws.bucket.name}/${aws.output} ${local.output}

# Change to standalone mode.
switch-standalone:
	cp config/standalone/*.xml ${hadoop.root}/etc/hadoop

# Change to pseudo-cluster mode.
switch-pseudo:
	cp config/pseudo/*.xml ${hadoop.root}/etc/hadoop

# Package for release.
distro:
	rm -f similarfiles.tar.gz
	rm -f similarfiles.zip
	rm -rf build
	mkdir -p build/deliv/similarfiles
	cp -r src build/deliv/similarfiles
	cp -r config build/deliv/similarfiles
	cp -r input build/deliv/similarfiles
	cp pom.xml build/deliv/similarfiles
	cp Makefile build/deliv/similarfiles
	cp README.txt build/deliv/similarfiles
	tar -czf similarfiles.tar.gz -C build/deliv similarfiles
	cd build/deliv && zip -rq ../../similarfiles.zip similarfiles
	