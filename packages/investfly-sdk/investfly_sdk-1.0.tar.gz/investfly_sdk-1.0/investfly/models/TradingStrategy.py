from abc import ABC, abstractmethod
from typing import List, Any, Dict

from investfly.models.MarketData import Security
from investfly.models.SecurityUniverseSelector import SecurityUniverseSelector
from investfly.models.StrategyModels import TradeSignal, StandardCloseCriteria
from investfly.models.PortfolioModels import TradeOrder, OpenPosition, Portfolio, PositionType
from investfly.utils.PercentBasedPortfolioAllocator import PercentBasedPortfolioAllocator


class TradingStrategy(ABC):

    def __init__(self) -> None:
        self.state: Dict[str, int | float | bool] = {}

    @abstractmethod
    def getSecurityUniverseSelector(self) -> SecurityUniverseSelector:
        pass

    """
    This function must be annotated with OnData to indicate when should this function be called.
    The function is called whenever a new data is available based on the subscribed data
    This function is called separately for each security
    @DataParams({
        "sma2":             {"datatype": DataType.INDICATOR, "indicator": "SMA", "barinterval": BarInterval.ONE_MINUTE,  "period": 2, "count": 2},
        "sma3":             {"datatype": DataType.INDICATOR, "indicator": "SMA", "barinterval": BarInterval.ONE_MINUTE, "period": 3, "count": 2},
        "allOneMinBars":    {"datatype": DataType.BARS, "barinterval": BarInterval.ONE_MINUTE},
        "latestDailyBar":   {"datatype": DataType.BARS, "barinterval": BarInterval.ONE_DAY, "count":1},
        "quote":            {"datatype": DataType.QUOTE},
        "lastprice":        {"datatype": DataType.QUOTE, "field": QuoteField.LASTPRICE},
        "allFinancials":    {"datatype": DataType.FINANCIAL},
        "revenue":          {"datatype": DataType.FINANCIAL, "field": FinancialField.REVENUE}

    })
    """
    @abstractmethod
    def evaluateOpenTradeCondition(self, security: Security, data: Dict[str, Any]) -> TradeSignal | None:
        pass

    def processOpenTradeSignals(self, portfolio: Portfolio, tradeSignals: List[TradeSignal]) -> List[TradeOrder]:
        portfolioAllocator = PercentBasedPortfolioAllocator(10, PositionType.LONG)
        return portfolioAllocator.allocatePortfolio(portfolio, tradeSignals)

    def getStandardCloseCondition(self) -> StandardCloseCriteria | None:
        # Note that these are always executed as MARKET_ORDER
        return None

    def evaluateCloseTradeCondition(self, openPos: OpenPosition, data) -> TradeOrder | None:
        return None

    def runAtInterval(self, portfolio: Portfolio) -> List[TradeOrder]:
        return []

    # These are optional methods that strategy can implement to track states between executions
    def getState(self) -> Dict[str, int | float | bool]:
        return self.state

    def restoreState(self, state: Dict[str, int | float | bool]) -> None:
        self.state = state
