from app.core.crud import CRUDBase
from app.models.admin import FieldWorkRecord
from app.schemas.field_work_record import FieldWorkRecordCreate, FieldWorkRecordUpdate

class FieldWorkRecordController(CRUDBase[FieldWorkRecord, FieldWorkRecordCreate, FieldWorkRecordUpdate]):
    def __init__(self):
        super().__init__(model=FieldWorkRecord)

field_work_record_controller = FieldWorkRecordController()
