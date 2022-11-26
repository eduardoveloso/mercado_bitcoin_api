import requests
import logging
from abc import ABC, abstractmethod
import datetime
from typing import List, Union
import json

#construir o log
#__name__ utilizará o nome do script para nomear o log
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MercadoBitcoinApi(ABC):
    def __init__(self, coin: str) -> None:
        self.coin = coin
        self.base_endpoint = 'https://www.mercadobitcoin.net/api'

    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        #metodo interno que nao sera acessivel externamente, nao estara exposto
        #metodo abstrato nao definido nessa classe
        pass

    def get_data(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f'Getting data from endpoint: {endpoint}')
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

class DaySummaryApi(MercadoBitcoinApi):
    type = 'day-summary'

    def _get_endpoint(self, date: datetime.date) -> str:
        return f'{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}'

class TradesApi(MercadoBitcoinApi):
    type = 'trades'

    def _get_unix_epoch(self, date: datetime.datetime) -> int:
        return int(date.timestamp())

    def _get_endpoint(self, date_from: datetime.datetime = None, date_to: datetime.datetime = None) -> str:
        
        if date_from and not date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            endpoint = f'{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}'
        elif date_from and date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            unix_date_to = self._get_unix_epoch(date_to)
            endpoint = f'{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}'
        else:
            endpoint = f'{self.base_endpoint}/{self.coin}/{self.type}'
        
        return endpoint

class DataWriter():
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def _write_row(self, row: str) -> None:
        with open(self.filename, 'a') as f:
            f.write(row)

    def write(self, data: Union[List, dict]) -> None:
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + '\n')
        if isinstance(data, List):
            for element in data:
                self.write(element)




# data = DaySummaryApi(coin='BTC').get_data(date=datetime.date(2022,11,21))
# writer = DataWriter('day_summary.json')
# writer.write(data)

data = TradesApi(coin='BTC').get_data(date_from=datetime.datetime(2022,11,21), date_to=datetime.datetime(2022,11,22))
writer = DataWriter('trades.json')
writer.write(data)