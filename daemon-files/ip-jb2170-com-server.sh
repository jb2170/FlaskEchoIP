#!/usr/bin/env -S bash -eu

source ./venv/bin/activate

exec gunicorn \
-b unix:/public${HOME}/sockets/ip-jb2170-com-server \
--log-file - \
FlaskEchoIP:app
