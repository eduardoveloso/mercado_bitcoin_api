import datetime
import json
from typing import List, Union
import os

class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, data) -> None:
        self.data = data
        self.message = f'Data type {type(data)} is not supported for ingestion'
        super().__init__(self.message)

class DataWriter():
    def __init__(self, coin: str, api: str) -> None:
        self.coin = coin
        self.api = api
        self.filename = f'{self.api}/{self.coin}/{datetime.datetime.now()}.json'

    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, 'a') as f:
            f.write(row)

    def write(self, data: Union[List, dict]) -> None:
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + '\n')
        elif isinstance(data, List):
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSupportedForIngestionException(data)