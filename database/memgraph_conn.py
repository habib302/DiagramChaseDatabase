from gqlalchemy import Memgraph
import os

MEMGRAPH_HOST = os.environ['MEMGRAPH_HOST']
MEMGRAPH_PORT = int(os.environ['MEMGRAPH_PORT'])
MEMGRAPH_USERNAME = 'fruitfulapproach@gmail.com'
# Place your Memgraph password that was created during Project creation
MEMGRAPH_PASSWORD = os.environ['MEMGRAPH_PASSWORD']

def get_memgraph(request=None):
    if request is None or (request is not None and 'memgraph' not in request.session):
        connection = Memgraph(host=MEMGRAPH_HOST, port=MEMGRAPH_PORT, username=MEMGRAPH_USERNAME, password=MEMGRAPH_PASSWORD, encrypted=True)
    
    if request is not None:
        request.session['memgraph'] = connection
        
    return connection
