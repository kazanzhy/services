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

#### Create database for Superset
* Create database  
`sudo -su postgres psql -c "CREATE DATABASE superset;"`  
* Create add user (set pass to superset_config.py)  
`sudo -su postgres psql -c "CREATE USER superset_user WITH PASSWORD 'superset_users_sofisticated_pass';"`  
`sudo -su postgres psql -c "ALTER USER superset_user WITH SUPERUSER;"`  
* Grant all privileges  
`sudo -su postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE superset TO superset_user;"`  
`sudo -su postgres psql -c "ALTER DATABASE superset OWNER TO superset_user;"`  

#### Set global variables
`echo "export PLATFORM_HOME=~/amon.platform" >> ~/.bashrc` 
`echo "export SUPERSET_HOME=~/amon.platform/superset" >> ~/.bashrc`  
`echo "export FLASK_APP='superset.app:create_app()'" >> ~/.bashrc`   
`echo "export PYTHONPATH='$SUPERSET_HOME:$PYTHONPATH'" >> ~/.bashrc`
`source ~/.bashrc`

#### Install and start Apache Superset
* Create separate venv  
`python3 -m venv venv_superset`  
`source venv_superset/bin/activate`  
* Install requirements  
`pip install --upgrade wheel pip`  
`pip install -r superset/requirements.txt`  
* Initialize the database  
`superset db upgrade`
* Create an admin user   
`superset fab create-admin --username amon --firstname Automatic --lastname Monitoring --email auto.monitoring@nszu.gov.ua --password 7S4a0NPE2fpFu26T`  
* Create user   
`superset fab create-user --role Public --username analyst --firstname Analyst --lastname NHSU --email analyst@nszu.gov.ua --password analyst_simple_pass`  
* Load some data to play with (optional)  
`superset load_examples`  
* Create default roles and permissions  
`superset init`
* Run service for debug (optional)  
`superset run -h '0.0.0.0' -p 8088 --with-threads --reload --debugger`  
* deactivate virtualenv  
`deactivate`  
* Start web-server using Gunicorn in systemd  
 (_gunicorn -c $SUPERSET_HOME/gunicorn_config.py "superset.app:create_app()"_)  
`sudo cp superset/superset.service /etc/systemd/system`  
`sudo systemctl daemon-reload`  
`sudo systemctl start superset.service`  
* Enable start after reboot  
`sudo systemctl enable superset.service`

##### Restart Superset  
`sudo systemctl stop superset.service`  
`sudo systemctl reset-failed superset.service`  
`sudo systemctl start superset.service`  

##### Upgrade Superset  
* Stop service  
`sudo systemctl stop superset.service`  
`sudo systemctl reset-failed superset.service`  
* Upgrade library in virtualenv  
`source $PLATFORM_HOME/venv_superset/bin/activate`  
`pip install --upgrade apache-superset`  
* Upgrade database  
`superset db upgrade`  
`superset init`  
* Deactivate virtualenv  
`deactivate`
* Start service  
`sudo systemctl start superset.service`  