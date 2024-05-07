from milvus import default_server
from pymilvus import connections, utility


default_server.start()

connections.connect(host="127.0.0.1", port=default_server.listen_port)

print(utility.get_server_version())

default_server.stop()
# milvus-server