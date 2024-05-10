from milvus import default_server
from pymilvus import connections, utility

default_server.start()

connections.connect(host="127.0.0.1", port="19530")

print(utility.get_server_version())

default_server.stop()
# milvus-server
