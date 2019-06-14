# Website Portfolio

Repository for portfolio website hosted with flask.

## Contents


Connect to VM:
```
gcloud compute --project "website-template-226613" ssh --zone "us-central1-a" "mauricerichard1991@website-prod" -- -R 52698:localhost:52698 -L 8000:localhost:8000
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

To add new website:
```
cd /etc/systemd/system/
cp website.service website2.service
# change name of directory 3 times
sudo systemctl start website2'
sudo systemctl enable website2'
sudo systemctl status website2'

sudo nano /etc/nginx/sites-available/default'
# Add new serverblock with servernam website2.com
```



