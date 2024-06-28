from typing import Set, List, Dict, Any

from investfly.api.RestApiClient import RestApiClient


class MarketDataApiClient:

    def __init__(self, restApiClient: RestApiClient) -> None:
        self.restApiClient = restApiClient

    def getNews(self, symbol: str) -> List[Dict[str, Any]]:
        return self.restApiClient.doGet(f"/symbol/news?symbols={symbol}")


    def getStandardSymbols(self, standardListName: str) -> Set[str]:
        return {"AAPL"}
