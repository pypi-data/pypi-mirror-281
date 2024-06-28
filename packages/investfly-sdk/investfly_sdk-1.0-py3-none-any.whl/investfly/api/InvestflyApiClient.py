import datetime

from investfly.api.MarketDataApiClient import MarketDataApiClient
from investfly.api.PortfolioApiClient import PortfolioApiClient
from investfly.api.RestApiClient import RestApiClient


class InvestflyApiClient:

    def __init__(self, baseUrl: str = "https://api.investfly.com"):
        self.restApiClient = RestApiClient(baseUrl)
        self.marketApi = MarketDataApiClient(self.restApiClient)
        self.portfolioApi = PortfolioApiClient(self.restApiClient)

    def login(self, username, password):
        return self.restApiClient.login(username, password)

    def logout(self):
        self.restApiClient.logout()

    @staticmethod
    def parseDatetime(date_str: str) -> datetime.datetime:
        return datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
