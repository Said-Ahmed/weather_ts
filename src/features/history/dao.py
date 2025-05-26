from src.features.history.models import History
from src.dao import BaseDAO


class HistoryDao(BaseDAO):
    model = History