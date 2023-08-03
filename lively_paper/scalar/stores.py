from typing import Dict

from clickhouse_connect import get_client
from clickhouse_connect.driver import Client

scalar_store: Client = get_client(host='127.0.0.1', port=8123, database='default')


def insert(table_name: str, data: Dict):
    scalar_store.insert(table=table_name, data=[list(data.values())], column_names=list(data.keys()))

