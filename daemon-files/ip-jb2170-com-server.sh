#!/bin/bash -e

exec ${HOME}/.local/var/lib/WSGIEchoIP/venv/bin/gunicorn \
-b unix:/public${HOME}/ip-jb2170-com-server \
--log-file - \
WSGIEchoIP:App
