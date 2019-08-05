# BigDataCourse
## Readme is available for each homework in respective directory
## About the course
The course aims to provide a broad understanding of big data and current technologies in managing and processing them with a focus on the urban environment.  With storage and networking getting significant cheaper and faster, big data sets could easily reach the hands of data enthusiasts with just a few mouse clicks. These enthusiasts could be policy makers, government employees or managers, who would like to draw insights and (business) value from big data. Thus, it is crucial for big data to be made available to the non-expert users in such a way that they can process the data without the need of a supercomputing expert. One such approach is to build big data programming frameworks that can deal with big data in as close a paradigm as the way it deals with “small data.” Also, such a framework should be as simple as possible, even if not as efficient as custom-designed parallel solutions. Users should expect that if their code works within these frameworks for small data, it will also work for big data. General topics of this course include: big data ecosystems, parallel and streaming programming model, MapReduce, Hadoop, Spark, Pig, and NoSQL solutions. Hands-on labs and exercises will be offered throughout to bolster the knowledge learned in each module.

## Tools used
- python2 or above
- Homework 5 and 6 are done NYU Hadoop Culster (called NYU dumbo)
# Installing Spark (unix and linux) (good luck to windows users)
- Step 1 : [Install Anaconda](https://www.anaconda.com/distribution/#download-section)
- Step 2: conda install pyspark
- run pyspark command in terminal, that should load pyspark shell.
- Note the install location using <b>pip show pyspark | grep Location</b>
- To write and run spark application in jupyter notebook enable pyspark shell in jupyter notebook
 by <b>export PYSPARK_DRIVER_PYTHON=`which jupyter`export PYSPARK_DRIVER_PYTHON_OPTS=notebookexport SPARK_HOME=[PySpark Location]/pyspark </b> in terminal or add in .bashrc in home directory in linux system.
 
