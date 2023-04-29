# /database/db/cassandra_cluster.py

from cassandra.cluster import Cluster
import logging
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table

# from cassandra.policies import DCAwareRoundRobinPolicy, TokenAwarePolicy

LOGGING = "<cassandra_cluster.py>\t\t| "


class CassandraCluster(object):
    """
    refer to `def connect()` below for default configuration
        database_ip = ['cassandra']: cassandra
        port = 9042
    This assumes you are on a network
    WHERE
        `nmap -sP 172.22.0.1/24`
    FROM inside this container
    YIELDS:
        cassandra.mist-alpha_MIST_server (172.22.0.2)
    DEFINED by
        connection.setup(database_ip, "cqlengine", protocol_version=3)
    """

    def __init__(self, ip=None, port=None):
        self.cluster = None
        self.port = port
        self.database_ip = ip

    def connect(self):
        logging.debug(f"{LOGGING} Connecting to cassandra database.")

        if self.port is None:
            self.port = 9042
        if self.database_ip is None:
            self.database_ip = ["database"]

        logging.info(
            f"{LOGGING} CLUSTER SETTINGS\t\t\t| database_ip({self.database_ip}): port({self.port})"
        )

        if isinstance(self.database_ip, list) and isinstance(self.port, int):
            self.cluster = Cluster(
                contact_points=self.database_ip,
                port=self.port,
                load_balancing_policy=None,
                protocol_version=3,
            )
            connection.setup(self.database_ip, "cqlengine", protocol_version=3)
        elif isinstance(self.database_ip, str) and isinstance(self.port, int):
            # dc_policy = DCAwareRoundRobinPolicy(cassDatacenter)
            # token_policy = TokenAwarePolicy(dc_policy)
            self.cluster = Cluster(
                contact_points=[self.database_ip],
                port=self.port,
                load_balancing_policy=None,
                protocol_version=3,
            )
            connection.setup([self.database_ip], "cqlengine", protocol_version=3)
        else:
            raise TypeError("Invalid arg `ip` or `port`: type(ip) is not (list, string) or type(port) is not (int).")

        online_cluster = self.cluster.connect()
        return online_cluster

    def shutdown(self):
        self.cluster.shutdown()

    def sync_tables(self, table=None):
        if table is None:
            raise Exception("Missing argument `table`")
        sync_table(table)