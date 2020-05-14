#!/bin/bash

/root/.pyenv/shims/uwsgi /var/www/uwsgi.ini
# && /usr/sbin/nginx -g 'daemon off;'