# mw_calc description
    Calculation of the Mann-Whitney test

# Install
    sudo apt-get update
    sudo apt-get install python3-pip
    sudo apt-get install r-base
    sudo apt-get install pandoc

# New env
    sudo -H pip3 install --upgrade pip
    sudo -H pip3 install virtualenv virtualenvwrapper

    echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
    echo "export WORKON_HOME=~/Env" >> ~/.bashrc
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
    source ~/.bashrc

    mkvirtualenv **project**

    (**project**) pip install -r requirements.txt
    (**project**) cd ~
    (**project**) git clone https://github.com/jenia0jenia/**project**.git
    (**project**) deactivate

    sudo apt-get install python3-dev
    sudo -H pip3 install uwsgi
    sudo mkdir -p /etc/uwsgi/sites
    sudo nano /etc/uwsgi/sites/**project**.ini

```
adduser **username**
passwd **username**
usermod -aG sudo www-data **username**
```

# /etc/uwsgi/sites/**project**.ini

    [uwsgi]
    project = **project**
    uid = **username**
    base = /home/%(uid)

    chdir = %(base)/%(project)
    home = %(base)/Env/%(project)
    module = %(project).wsgi:application

    req-logger = file:/tmp/uwsgi/reqlog # chown **username**:www-data /tmp/uwsgi/reqlog
    logger = file:/tmp/uwsgi/errlog # chown **username**:www-data /tmp/uwsgi/errlog

    master = true
    processes = 5

    socket = /run/uwsgi/%(project).sock # chown **username**:www-data /run/uwsgi/%(project).sock
    chown-socket = %(uid):www-data
    chmod-socket = 660
    vacuum = true

# /etc/systemd/system/uwsgi.service

    [Unit]
    Description=uWSGI Emperor service

    [Service]
    ExecStartPre=/bin/bash -c 'mkdir -p /run/uwsgi; chown **username**:www-data /run/uwsgi'
    ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/sites
    Restart=always
    KillSignal=SIGQUIT
    Type=notify
    NotifyAccess=all

    [Install]
    WantedBy=multi-user.target

# nginx
    sudo apt-get install nginx
    sudo nano /etc/nginx/sites-available/**project**

    
    server {
        listen 443 ssl; # managed by Certbot
        server_name **sitename**;

        access_log    /home/**sitename**/logs/accsess.log;
        error_log     /home/**sitename**/logs/error.log;

        gzip            on;
        gzip_min_length 1000;
        gzip_proxied    expired no-cache no-store private auth;
        gzip_types      text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript application/javascript;

        location = /favicon.ico { access_log off; log_not_found off; }

        location /static/ {
            root /home/**sitename**/**project**;
        }

        location / {
            include         uwsgi_params;
            uwsgi_pass      unix:/run/uwsgi/**project**.sock;

            # Добавить условие для отсечения ботов
            if ( $host !~* ^(yourdomain.com|www.yourdomain.com)$ ) {
               return 444;
            }
        }
        
        ssl_certificate /etc/letsencrypt/live/**sitename**/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/**sitename**/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
    }

    server {
        listen 80;
        server_name **sitename** www.**sitename**;
        return 301 https://**sitename**$request_uri;
    }

    server {
        listen 443;
        server_name www.**sitename**;
        return 301 https://**sitename**$request_uri;
    }


    sudo ln -s /etc/nginx/sites-available/**project** /etc/nginx/sites-enabled

# R Packages
    R
    install.packages(c('readxl', 'tibble', 'rjson', 'jsonlite', 'rmarkdown', 'readr', 'knitr', 'xlsx', 'nortest', 'psych'), dependencies = TRUE)
    q() y



# TODO ()

1. Сохранять данные по группам в сессии


# Для добавления нового калькулятора:

    ```
    python manage.py startapp new_calc
    ```

    settings.py

        PLANFIX_CALCS = {
            ...
            new_calc
            ...
        }



    ```
    mkdir ~/mw_calc/new_calc/templates/new_calc/
    mkdir ~/mw_calc/new_calc/static/new_calc/

    mkdir ~/mw_calc/script/new_calc/

    mkdir ~/mw_calc/tmp/new_calc/
    mkdir ~/mw_calc/tmp/new_calc/docx/
    mkdir ~/mw_calc/tmp/new_calc/json/
    mkdir ~/mw_calc/tmp/new_calc/html/
    mkdir ~/mw_calc/tmp/new_calc/xlsx/
    ```
