from typing import Optional, List

from fastapi import APIRouter,Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from odoo.api import Environment
from odoo.exceptions import AccessError, MissingError, AccessDenied

from odoo_fastapi.src.user_management.schemas import User
from odoo_fastapi.src.employee_management.schemas import Employee
from odoo_fastapi.project.dependency import odoo_env
from odoo_fastapi.src.user_management.utils import get_current_active_user


router = APIRouter()


@router.get("/employees", response_model=List[Employee])
def employees(domain: Optional[str] = [], env: Environment = Depends(odoo_env), current_user: User = Depends(get_current_active_user)):
    employees_list = env["employee.model"].search(domain)
    # breakpoint()
    return [Employee.from_employee(e) for e in employees_list]


@router.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: int, env: Environment = Depends(odoo_env), current_user: User = Depends(get_current_active_user)):
    try:
        employee = env["employee.model"].browse(employee_id)
        return Employee.from_employee(employee)
    except MissingError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    except AccessError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN)


@router.post("/employees", response_model=Employee, status_code=HTTP_201_CREATED)
def create_employee(employee: Employee, env: Environment = Depends(odoo_env), current_user: User = Depends(get_current_active_user)):
    employee = env["employee.model"].create(
        {
            "user_id": employee.user_id,
            "username": employee.username,
            "email": employee.email,
            "gender": employee.gender,
            "mobile_no": employee.mobile_no,
            "active": employee.active,
            "dob": employee.dob,
            "age": employee.age,
            "name": employee.name,
            "manager_id": employee.manager_id,

        }
    )
    return Employee.from_employee(employee)


@router.patch("/employees/{employee_id}", status_code=HTTP_201_CREATED)
def update_employee(employee: Employee, employee_id: int, env: Environment = Depends(odoo_env), current_user: User = Depends(get_current_active_user)):
    employee_data = env["employee.model"].browse(employee_id)
    employee_partial_data = employee.dict(exclude_unset=True)
    employee_data.write(employee_partial_data)
    return employee_partial_data


@router.delete("/employees/{employee_id}", status_code=HTTP_201_CREATED)
def update_employee(employee_id: int, env: Environment = Depends(odoo_env), current_user: User = Depends(get_current_active_user)):
    breakpoint()
    employee_data = env["employee.model"].browse(employee_id)
    employee_data.unlink()
    return "Employee Deleted"


