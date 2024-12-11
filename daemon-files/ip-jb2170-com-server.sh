#!/bin/bash -eu

exec ${HOME}/.local/var/lib/FlaskEchoIP/venv/bin/gunicorn \
-b unix:/public${HOME}/sockets/ip-jb2170-com-server \
--log-file - \
FlaskEchoIP:app
