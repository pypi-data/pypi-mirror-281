from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta, datetime
from enum import Enum
from typing import Any, Dict

from investfly.models.ModelUtils import ModelUtils


@dataclass
class DatedValue:
    date: datetime
    value: float | int

    def toJsonDict(self) -> Dict[str, Any]:
        return {
            'date': ModelUtils.formatDatetime(self.date),
            'value': self.value
        }

    @staticmethod
    def fromDict(json_dict: Dict[str, Any]) -> DatedValue:
        return DatedValue(ModelUtils.parseDatetime(json_dict['date']), json_dict['value'])


class TimeUnit(str, Enum):
    MINUTES = "MINUTES"
    HOURS = "HOURS"
    DAYS = "DAYS"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


@dataclass
class TimeDelta:
    value: int
    unit: TimeUnit

    def toPyTimeDelta(self) -> timedelta:
        totalMinutes = self.value
        if self.unit == TimeUnit.HOURS:
            totalMinutes = totalMinutes * 60
        elif self.unit == TimeUnit.DAYS:
            totalMinutes = totalMinutes * 60 * 24

        return timedelta(minutes=totalMinutes)

    def toDict(self) -> Dict[str, Any]:
        return self.__dict__.copy()

    @staticmethod
    def fromDict(json_dict: Dict[str, Any]) -> TimeDelta:
        return TimeDelta(json_dict['value'], TimeUnit[json_dict['unit']])



@dataclass
class Session:
    username: str
    clientId: str
    clientToken: str

    @staticmethod
    def fromJsonDict(json_dict: Dict[str, Any]) -> Session:
        return Session(json_dict['username'], json_dict['clientId'], json_dict['clientToken'])
