# -*- coding: utf-8 -*-

import Pyjo.Server.Daemon
import Pyjo.URL
from Pyjo.Util import b

import os

OPENSHIFT_REPO_DIR = os.environ['OPENSHIFT_REPO_DIR']
os.chdir(OPENSHIFT_REPO_DIR)

OPENSHIFT_PYTHON_IP = os.environ['OPENSHIFT_PYTHON_IP']
OPENSHIFT_PYTHON_PORT = os.environ['OPENSHIFT_PYTHON_PORT']

listen = str(Pyjo.URL.new(scheme='http', host=OPENSHIFT_PYTHON_IP, port=OPENSHIFT_PYTHON_PORT))

daemon = Pyjo.Server.Daemon.new(listen=[listen])
daemon.unsubscribe('request')


DATA = r'''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Pyjoyment</title>
</head>

<body>
<h1>♥ Pyjoyment ♥</h1>
<h2>This page is served by Pyjoyment framework.</h2>
<p>{method} request for {path}</p>
<p>See <a href="http://pyjoyment.readthedocs.org/">http://pyjoyment.readthedocs.org/</a>
and <a href="https://github.com/dex4er/Pyjoyment">https://github.com/dex4er/Pyjoyment</a></p>
</body>

</html>
'''


@daemon.on
def request(daemon, tx):
    # Request
    method = tx.req.method
    path = tx.req.url.path

    # Response
    tx.res.code = 200
    tx.res.headers.content_type = 'text/html; charset=utf-8'
    tx.res.body = b(DATA.format(method=method, path=path))

    # Resume transaction
    tx.resume()


daemon.run()
