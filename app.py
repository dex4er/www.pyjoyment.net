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


@daemon.on
def request(daemon, tx):
    # Request
    method = tx.req.method
    path = tx.req.url.path

    # Response
    tx.res.code = 200
    tx.res.headers.content_type = 'text/plain'
    tx.res.body = b("{0} request for {1}\n".format(method, path))

    # Resume transaction
    tx.resume()


daemon.run()
