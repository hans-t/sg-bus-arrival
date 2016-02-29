#!/bin/bash


for var in SITENAME API_KEY UNIQUE_USER_ID; do
    if ! [ -n "${!var}" ]; then
        echo "$var environment variable is not set."
        exit 1
    fi
done

export ROOT=~/sites/$SITENAME


## Install required libraries
sudo apt-get update
sudo apt-get install -y python3 python3-pip git nginx supervisor


## Change to root directory, create required folders
mkdir -p $ROOT
cd $ROOT
rm -rf source
mkdir -p logs


## Create Python virtual environment, clone Github repo and install Python packages
python3 -m venv --copies --clear venv
source venv/bin/activate
git clone https://github.com/hans-t/sg-bus-arrival.git source
pip install -r source/requirements.txt


## Populate variables in files
cd source/deployment
envsubst < credentials.py > ../app/credentials.py
DOLLAR=$ envsubst < nginx_template.conf > nginx-$SITENAME.conf
DOLLAR=$ envsubst < supervisor_template.conf > supervisor-$SITENAME.conf
sed -e s/'$SITENAME'/$SITENAME/g gunicorn_start_template.sh > gunicorn_start.sh

sudo cp nginx-$SITENAME.conf /etc/nginx/sites-available/$SITENAME.conf
sudo cp supervisor-$SITENAME.conf /etc/supervisor/conf.d/$SITENAME.conf


## make gunicorn script executable
sudo chmod u+x gunicorn_start.sh


## symlink configurations
sudo ln -sf /etc/nginx/sites-available/$SITENAME.conf /etc/nginx/sites-enabled/$SITENAME.conf

## Restart services
sudo service nginx stop
sudo service nginx start
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start gunicorn