from app.core.crud import CRUDBase
from app.models.admin import DutyStaff
from app.schemas.duty_staff import DutyStaffCreate, DutyStaffUpdate

class DutyStaffController(CRUDBase[DutyStaff, DutyStaffCreate, DutyStaffUpdate]):
    def __init__(self):
        super().__init__(model=DutyStaff)

duty_staff_controller = DutyStaffController()