#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Pyjo.Server.Daemon
import Pyjo.URL

from Pyjo.Loader import embedded_file
from Pyjo.Util import b, u

import os
import pkg_resources
import sys

OPENSHIFT_REPO_DIR = os.environ['OPENSHIFT_REPO_DIR']
os.chdir(OPENSHIFT_REPO_DIR)

OPENSHIFT_PYTHON_IP = os.environ['OPENSHIFT_PYTHON_IP']
OPENSHIFT_PYTHON_PORT = os.environ['OPENSHIFT_PYTHON_PORT']

VERSION = pkg_resources.get_distribution('Pyjoyment').version

listen = str(Pyjo.URL.new(scheme='http', host=OPENSHIFT_PYTHON_IP, port=OPENSHIFT_PYTHON_PORT))

daemon = Pyjo.Server.Daemon.new(listen=[listen])
daemon.unsubscribe('request')


DATA = u(r'''
@@ index.html.tpl
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Pyjoyment</title>
</head>

<body>
<h1>♥ Pyjoyment ♥</h1>
<h2>This page is served by Pyjoyment {version} framework.</h2>
<p>{method} request for {path}</p>
<p>See <a href="http://pyjoyment.readthedocs.org/">http://pyjoyment.readthedocs.org/</a>
and <a href="https://github.com/dex4er/Pyjoyment">https://github.com/dex4er/Pyjoyment</a></p>
<p>See <a href="https://github.com/dex4er/www.pyjoyment.net/blob/master/app.py">app.py</a> source file.</p>
</body>

</html>
''')


@daemon.on
def request(daemon, tx):
    version = VERSION

    # Request
    method = tx.req.method
    path = tx.req.url.path

    # Template
    template = embedded_file(sys.modules[__name__], 'index.html.tpl')

    # Response
    tx.res.code = 200
    tx.res.headers.content_type = 'text/html; charset=utf-8'
    tx.res.body = b(template.format(**locals()))

    # Resume transaction
    tx.resume()


daemon.run()
