#### Prepare CentOS server 
* Update system  
`sudo dnf -y update`  
`sudo dnf -y groupinstall "Development Tools"`
* Install system requirements  
`sudo dnf -y install wget git gcc gcc-c++ bzip2-devel openssl-devel`  
`sudo dnf -y install libpq-devel libffi-devel cyrus-sasl-devel openldap-devel`   
* Install Python 3.8, create link to `python3`  
`sudo dnf -y install python38 python38-devel`   
`sudo alternatives --set python3 /usr/bin/python3.8`  
* Reinstall Python 3.8 libs (optional)  
`sudo dnf -y reinstall python3-setuptools python3-pip python3-wheel`  
`pip3 install --upgrade wheel setuptools pip virtualenv`

* Install Java  
`sudo dnf -y install java-11-openjdk`  
`sudo alternatives --set java java-11-openjdk.x86_64`  
* Install Scala  
`sudo dnf -y install scala`  
If `scala -version` not 2.12.x then:  
`sudo dnf -y remove scala`  
`wget https://www.scala-lang.org/files/archive/scala-2.12.12.rpm`  
`sudo dnf -y install scala-2.12.12.rpm`  
`rm -f scala-2.12.12.rpm`

#### Set global variables  
`echo "export PLATFORM_HOME=~/amon.platform" >> ~/.bashrc` 
`echo "export JAVA_HOME=$(dirname $(dirname $(readlink $(readlink $(which javac)))))" >> ~/.bashrc`  
`echo "export CLASSPATH=$CLASSPATH:/usr/local/spark/jars" >> ~/.bashrc`
`echo "export SPARK_HOME=/usr/local/spark" >> ~/.bashrc`  
`echo "export SPARK_DAEMON_CLASSPATH=/usr/local/spark/jars" >> ~/.bashrc`  
`echo "export SPARK_LOG_DIR='$PLATFORM_HOME/spark/logs'" >> ~/.bashrc`  
`echo "export SPARK_PID_DIR='$PLATFORM_HOME/spark/pids'" >> ~/.bashrc`  
`echo "export SPARK_WORKER_DIR='$PLATFORM_HOME/spark/workers'" >> ~/.bashrc`  
`echo "export SPARK_MASTER_WEBUI_PORT=7070" >> ~/.bashrc`  
`echo "export PYSPARK_PYTHON=/usr/bin/python3" >> ~/.bashrc`  
`echo "export PYSPARK_DRIVER_PYTHON=/usr/bin/python3" >> ~/.bashrc`  
`echo "export PATH=$PATH:/usr/local/spark/bin" >> ~/.bashrc`  
`source ~/.bashrc`


#### Install and start Apache Spark   
* Download  
`wget https://downloads.apache.org/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz`  
`tar -xf spark-3.0.1-bin-hadoop3.2.tgz`  
* Move to system path  
`sudo mkdir /usr/local/spark`  
`sudo cp -r spark-3.0.1-bin-hadoop3.2/* /usr/local/spark`  
* Remove temp files  
`rm -f spark-3.0.1-bin-hadoop3.2.tgz`
`rm -rf spark-3.0.1-bin-hadoop3.2`
* Copy to systemd folder  
`sudo cp spark/*.service /etc/systemd/system`  
* Reload systemctl  
`sudo systemctl daemon-reload`  
`sudo systemctl start spark-master.service`  
`sudo systemctl start spark-slave.service`  
* Enable start after reboot  
`sudo systemctl enable spark-master.service`  
`sudo systemctl enable spark-slave.service`  
* Install JDBC Driver for Postgres (optional)  
`wget https://jdbc.postgresql.org/download/postgresql-42.2.18.jar`  
`sudo mv postgresql-42.2.18.jar /usr/local/spark/jars/`  

##### Restart Spark
`sudo systemctl restart spark-master.service`