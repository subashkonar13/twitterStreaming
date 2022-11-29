# Description
Docker Image for Twitter Streaming with Python,Adminer and Postgress

## Description
The objective is to ingest the data from Twitter and write in real time to Postgres and view it using adminer
I have developed this image keeping in mind that it will handle this job as a single container.It can be further scaled by using docker-compose and customise the configs.
The folder/file structure is as below:

![enter image](https://raw.githubusercontent.com/subashkonar13/evaluation/main/images/file2.jpg)

 - `input`-Input folder for csv files 
 - `output`- output folder
 - `docker-compose.yml` is optional in case if the container config is required and the job has to be submitted at scale.
 - `etl.py` is the python script which perform the ETL job
 - `func`-folder holds the individual python function to read,transform and write.
 - `Dockerfile`
 - `requirements.txt`

## Prerequisites
1. Install Docker Desktop.
2. Install Apache Parquet Viewer from [here](https://apps.microsoft.com/store/detail/apache-parquet-viewer/9PGB0M8Z4J2T?hl=en-us&gl=us) 

**Note**: I am using Windows 11 to perform the installations.

## Task to be performed:
3. Run `docker pull subashkonar13/evaluation:latest`
![enter image description here](https://raw.githubusercontent.com/subashkonar13/evaluation/main/images/pull.jpg)
4. Then Run `docker run  subashkonar13/evaluation:latest driver local:///opt/application/etl.py`.Currently its getting deployed in client mode.
![execute](https://raw.githubusercontent.com/subashkonar13/evaluation/main/images/execute.jpg)
5. Get the **container name** attached to the image by running command `docker ps -a --format="container:{{.ID}} image:{{.Image}}"` 
![enter image description here](https://raw.githubusercontent.com/subashkonar13/evaluation/main/images/run.jpg)
Since I am using windows OS,I would need to explicitly copy the files to host. In case of linux, the drive from linux host can be mounted easily to docker container path and files can be viewed from the host.
7. To copy the files to current host run (get the container name as in attached image from previous command) `docker cp <container name>:/opt/application/output C:/HD/`

![test](https://raw.githubusercontent.com/subashkonar13/evaluation/main/images/file.jpg)

8. Once the files  are copied,you can open the file in `Apache Parquet viewer`
![enter image description here](https://raw.githubusercontent.com/subashkonar13/evaluation/main/images/parquetview.jpg)

