"""Gunicorn *development* config file"""

# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "main.wsgi:application"
# The granularity of Error log outputs
loglevel = "debug"
# The number of worker processes for handling requests
workers = 7
# The socket to bind
bind = "127.0.0.1:4000"
# Restart workers when code changes (development only!)
reload = False
# Write access and error info to /var/log
accesslog = errorlog = "/var/gunicorn-tor.log"
# Redirect stdout/stderr to log fil
capture_output = True
# PID file so you can easily fetch process ID
pidfile = "/var/gunicorn-tor.pid"
# Daemonize the Gunicorn process (detach & enter background)
daemon = False