from app.database.models.employee_model import EmployeePublic
from app.database.models.vacation_request_model import VacationRequestPublic


class SubordinateRequestPublic(VacationRequestPublic):
    employee: "EmployeePublic"
