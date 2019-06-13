# Website_Template

This page will describe how to set up a new flask based website within 1 hour.

## Contents
Automate deployment





## Set up from template
- Standard Image
- 


## How to create template

Design is shown in the picture below:  
![image](https://gitlab.com/MR1991/website_template/wikis/uploads/021b18f12229fba2a5dd3004b91d023a/image.png)

### Set up Compute Engine
Go to google cloud and create a new project.
Within the project create a new compute engine with settings:  
```
1v CPU  3.75 GB memory  
Boot disk Debian 9
Allow full access to all Cloud APIs  
Allow HTTP traffic  
Allow HTTPS traffic  
```
Go to External IP Addresses, change to static.  
Go to Firewall rules. Ingress, Allow, Source Ip ranges: 0.0.0.0/0, Specified protocols and ports, tcp: 52698.

On local computer:
* Install google cloud SDK shell locally https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe  
* Install putty https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html  
* Install atom from https://atom.io/  
* In Atom on the homepage "install packages -> remote atom", then "packages -> remote atom -> start server".  
* Start up the google cloud SDK shell. Do the below two things. Replace project, user@x and zone.   

```
gcloud init
gcloud compute --project "website-template-226613" ssh --zone "us-east1-b" "mauricerichard1991@website" -- -R 52698:localhost:52698 -L8000:localhost:8000
```

On compute engine:
```
sudo curl -o /usr/local/bin/rmate https://raw.githubusercontent.com/aurora/rmate/master/rmate
sudo chmod +x /usr/local/bin/rmate
sudo mv /usr/local/bin/rmate /usr/local/bin/ratom
```
Then use sudo ratom example.txt command on compute engine to edit files locally.

### Install modules and create virtual environment 
Install Python3.7
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install virtualenv
sudo apt-get install python-pip
sudo apt-get dist-upgrade
sudo apt-get install build-essential checkinstall python-dev python-setuptools python-pip python-smbus
sudo apt-get install libffi-dev libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev zlib1g-dev openssl 
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
sudo tar xzf Python-3.7.0.tgz
cd Python-3.7.0
sudo ./configure --enable-optimizations
sudo make altinstall
python3.7 -V
```

Install Git(version control), flask (application), gunicorn (WSGI server) and nginx (Web Server).
Create virtual environment to work in.
```
sudo apt-get install git
sudo apt-get install gunicorn
sudo apt-get install nginx
virtualenv --python python3.7 venv
source venv/bin/activate
pip install wheel
pip install cookiecutter
pip install flask 
pip install gunicorn
```

### Create project folder structure
Create project
```
All files
run.py	This is the file that is invoked to start up a development server. It gets a copy of the app from your package and runs it. This won’t be used in production, but it will see a lot of mileage in development.
requirements.txt	This file lists all of the Python packages that your app depends on. You may have separate files for production and development dependencies.
config.py	This file contains most of the configuration variables that your app needs.
/instance/config.py	This file contains configuration variables that shouldn’t be in version control. This includes things like API keys and database URIs containing passwords. This also contains variables that are specific to this particular instance of your application. For example, you might have DEBUG = False in config.py, but set DEBUG = True in instance/config.py on your local machine for development. Since this file will be read in after config.py, it will override it and set DEBUG = True.
/yourapp/	This is the package that contains your application.
/yourapp/__init__.py	This file initializes your application and brings together all of the various components.
/yourapp/views.py	This is where the routes are defined. It may be split into a package of its own (yourapp/views/) with related views grouped together into modules.
/yourapp/models.py	This is where you define the models of your application. This may be split into several modules in the same way as views.py.
/yourapp/static/	This directory contains the public CSS, JavaScript, images and other files that you want to make public via your app. It is accessible from yourapp.com/static/ by default.
/yourapp/templates/	This is where you’ll put the Jinja2 templates for your app.
```

### Set up external web hosting
Create entrypoint to flask app. This will tell our Gunicorn server how to interact with the application.

```nano ~/website/wsgi.py```
```
from myproject import app

if __name__ == "__main__":
    app.run()
```

Set up a startup service  
```sudo nano /etc/systemd/system/website.service```

```
[Unit]
Description=Gunicorn instance to serve website
After=network.target

[Service]
User=mauricerichard1991
Group=www-data
WorkingDirectory=/home/mauricerichard1991/website
Environment="PATH=/home/mauricerichard1991/website/venv/bin"
ExecStart=/home/mauricerichard1991/website/venv/bin/gunicorn --workers 3 --bind unix:website.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```
```
sudo systemctl start website
sudo systemctl enable website
sudo systemctl status website
```


Set up nginx
```
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup
```
``` sudo nano /etc/nginx/sites-available/default ```
```
server {
	listen 80 default_server;
	listen [::]:80 default_server;

	root /var/www/html;

	index index.html index.htm index.nginx-debian.html;

	server_name _;

	location / {
		include proxy_params;
		proxy_pass http://unix:/home/mauricerichard1991/website/website.sock;
	}

}
```
```
sudo nginx -t
sudo systemctl restart nginx
```

### Website Domain




### Set up HTTPS 
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04


Set up aliases 
```

cat > ~/.bash_aliases <<EOF
alias alias1='sudo nano ~/.bash_aliases'
alias alias2='sudo source ~/.bashrc'
EOF



```





```
requirements.txt
run.py
config/
  __init__.py # Empty, just here to tell Python that it's a package.
  default.py
  production.py
  development.py
  staging.py
instance/
  config.py
yourapp/
  __init__.py
  models.py
  views.py
  static/
  templates/

```

```
import os
from flask import Flask, send_file
app = Flask(__name__)


@app.route("/hello")
def hello():
    return "Hello World from Flask"


@app.route("/")
def main():
    index_path = os.path.join(app.static_folder, 'index.html')
    return send_file(index_path)


# Everything not declared before (not a Flask route / API endpoint)...
@app.route('/<path:path>')
def route_frontend(path):
    # ...could be a static file needed by the front end that
    # doesn't use the `static` path (like in `<script src="bundle.js">`)
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    # ...or should be handled by the SPA's "router" in front end
    else:
        index_path = os.path.join(app.static_folder, 'index.html')
        return send_file(index_path)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
```



```




