from app.core.crud import CRUDBase
from app.models.admin import TotalRecord
from app.schemas.total import TotalRecordCreate, TotalRecordUpdate

class TotalRecordController(CRUDBase[TotalRecord, TotalRecordCreate, TotalRecordUpdate]):
    def __init__(self):
        super().__init__(model=TotalRecord)



total_record_controller = TotalRecordController()

