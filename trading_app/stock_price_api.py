from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import requests


class WrongStockShortName(Exception):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"stock: {self.name} does not exist")


class APILimitReached(Exception):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__("Our API limit is reached, please wait a few minutes and try again")



class BaseAPI(ABC):
    @abstractmethod
    def get_price(self, name: str) -> float:
        pass


class PolygonAPI(BaseAPI):
    def __init__(self, token: str) -> None:
        self.token = token
    
    def get_price(self, name: str) -> float:
        yesterday = datetime.now() - timedelta(1)
        yesterday = datetime.strftime(yesterday, "%Y-%m-%d")
        url = f"https://api.polygon.io/v1/open-close/{name}/{yesterday}?adjusted=true&apiKey={self.token}"
        r = requests.get(url)
        data = r.json()
        print(data)
        if data["status"] == "ERROR":
            raise APILimitReached()
        elif data["status"] == "NOT_FOUND":
            raise WrongStockShortName(name)
        else:
            return data["close"]