from typing import Union, Optional
from pydantic import BaseModel
from datetime import date
from odoo.models import Model



class Employee(BaseModel):

    id: Optional[int]
    user_id: Optional[int]
    username: Optional[str]
    email: Optional[str]
    gender: Optional[str]
    mobile_no: Optional[int]
    active: bool = False
    dob: Optional[date]
    age: Optional[int]
    name: Optional[str]
    manager_id: Optional[int]
    # skills : Optional[List]

    @classmethod
    def from_employee(cls, e: Model) -> "Employee":
        return Employee(id=e.id, user_id=e.user_id, username=e.username, email=e.email, gender=e.gender, mobile_no=e.mobile_no, active=e.active, dob=e.dob, age=e.age, name=e.name, manager_id=e.manager_id)
