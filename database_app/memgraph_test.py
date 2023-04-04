from gqlalchemy import Memgraph

MEMGRAPH_HOST = '13.52.221.133'
MEMGRAPH_PORT = 7687
MEMGRAPH_USERNAME = 'fruitfulapproach@gmail.com'
# Place your Memgraph password that was created during Project creation
MEMGRAPH_PASSWORD = 'LunaMoona12340235ShebaHut$$'

def hello_memgraph(host: str, port: int, username: str, password: str):
    connection = Memgraph(host, port, username, password, encrypted=True)
    results = connection.execute_and_fetch(
        'CREATE (n:FirstNode { message: "Hello Memgraph from Python!" }) RETURN n.message AS message'
    )
    print("Created node with message:", next(results)["message"])

if __name__ == "__main__":
    hello_memgraph(MEMGRAPH_HOST, MEMGRAPH_PORT, MEMGRAPH_USERNAME, MEMGRAPH_PASSWORD)