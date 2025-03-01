from fastapi.routing import APIRoute

from app.core.crud import CRUDBase
from app.log import logger
from app.models.admin import TransactionRecord
from app.schemas.transactions import TransactionCreate, TransactionUpdate


class ApiController(CRUDBase[TransactionRecord, TransactionCreate, TransactionUpdate]):
    def __init__(self):
        super().__init__(model=TransactionRecord)


api_controller = ApiController()
