#!/bin/bash

uwsgi -H /usr/local/bin/python3.6 --ini uwsgi.ini && /usr/sbin/nginx -g 'daemon off;'