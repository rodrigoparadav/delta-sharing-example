from delta_sharing.delta_sharing import SharingClient
from delta_sharing.reader import DeltaSharingReader
from delta_sharing.rest_client import DataSharingRestClient
from typing import List

from log import Log

log = Log().get_instance()


class TableDoesNotExistError(Exception):
    """Trigger when the Table requested is not part of the share"""

    def __init__(self, table_name):
        self.table_name = table_name
        self.message = f"Table {self.table_name} does not exist in the share!!"
        super().__init__(self.message)


class Share:
    """Manage the list of tables"""

    def __init__(self, name=None, tables=None):
        self.name = name
        self.tables_name = {table.name for table in tables}
        [self.__setattr__(table.name, table) for table in tables]

    def __repr__(self) -> str:
        return f"Share : {self.name} Tables : {self.tables_name}"


class DeltaShareClient:
    def __init__(self, profile_file):
        self._credentials_file = profile_file
        self.client = SharingClient(profile_file)
        self._rest_api = DataSharingRestClient(self.client.__dict__.get("_profile"))
        self.shares = self._build_shares()
        self.table_index = {
            table_name: share
            for share in self.shares
            for table_name in share.tables_name
        }

    def _build_shares(self):
        return [
            Share(
                name=share.name,
                tables=self.client._SharingClient__list_all_tables_in_share(share),
            )
            for share in self.client.list_shares()
        ]

    def get_list_of_tables(self) -> List[str]:
        """
            Get the list of table available in the share
        :return: list, table names  available in the share
        """
        return [table.name for table in self.client.list_all_tables()]

    def get_table(
        self, table_name, limit=None, version=None, timestamp=None
    ) -> DeltaSharingReader:
        """
        Get table from specific share

        :param table_name: name of the table to return data
        :param limit: amount of data to return, defaults to 100
        :param version: _description_, defaults to None
        :param timestamp: _description_, defaults to None
        :return: _description_
        """
        if table_name not in self.table_index:
            return TableDoesNotExistError(table_name=table_name)
        return DeltaSharingReader(
            table=getattr(self.table_index.get(table_name), table_name),
            rest_client=self._rest_api,
            limit=limit,
            version=version,
            timestamp=timestamp,
        )

    def __repr__(self) -> str:
        return f"{self.shares}"
