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

#### Install and start Postgres  
as database for meta information
* Select version  
`sudo dnf module enable postgresql:12`  
* Install Postgres  
`sudo dnf -y install postgresql postgresql-server`  
* Start Postgres  
`postgresql-setup --initdb`  
`sudo systemctl start postgresql`  
`sudo systemctl enable postgresql`  

#### Create database for Airflow
* Create database  
`sudo -su postgres psql -c "CREATE DATABASE airflow;"`  
* Create add user (set pass to airflow.cfg)  
`sudo -su postgres psql -c "CREATE USER airflow_user WITH PASSWORD 'airflow_users_sofisticated_pass';"`  
`sudo -su postgres psql -c "ALTER USER airflow_user WITH SUPERUSER;"`  
* Grant all privileges  
`sudo -su postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow_user;"`  
`sudo -su postgres psql -c "ALTER DATABASE airflow OWNER TO airflow_user;"`  

#### Set global variables
`echo "export PLATFORM_HOME=~/amon.platform" >> ~/.bashrc` 
`echo "export AIRFLOW_HOME=~/amon.platform/airflow" >> ~/.bashrc`
`echo "export PYTHONPATH='$AIRFLOW_HOME:$PYTHONPATH'" >> ~/.bashrc`  
`source ~/.bashrc`

#### Install and start Apache Airflow   
* Create virtualenv  
`python3 -m venv venv_airflow`  
`source venv_airflow/bin/activate`  
* Install requirements  
`pip install --upgrade wheel pip setuptools`  
`pip install -r requirements.txt`  
* Initialize database  
`airflow db init `  
* Create admin user  
`airflow users create -r Admin -u amon -e auto.monitoring@mail.gov.ua -f Automatic -l Monitoring -p 7S4a0NPE2fpFu26T`
* Create user  
`airflow users create -r User -u analyst -e analyst@mail.gov.ua -f Analyst -l NHSU -p analyst_simple_pass`
* deactivate virtualenv  
`deactivate`  
* Start scheduler and webserver daemons in systemd  
_airflow webserver -D && airflow scheduler -D_  
`sudo cp airflow/airflow.service /etc/systemd/system`  
`sudo systemctl daemon-reload`  
`sudo systemctl start airflow.service`   
* Enable start after reboot  
`sudo systemctl enable airflow.service`

##### Restart Airflow  
`sudo systemctl stop airflow.service`  
`sudo systemctl reset-failed airflow.service`  
`sudo systemctl start airflow.service`  

##### Upgrade Airflow  
* Stop service  
`sudo systemctl stop superset.service`  
`sudo systemctl reset-failed superset.service`  
* Upgrade library in virtualenv  
`source $PLATFORM_HOME/venv_superset/bin/activate`  
`pip install --upgrade apache-airflow`  
* Upgrade database  
`airflow db upgrade`  
`airflow db init`  
* Deactivate virtualenv  
`deactivate`
* Start service  
`sudo systemctl start airflow.service`  