# gere um enum para o tipo de usuário

from enum import Enum

class UserType(Enum):
    CUSTOMER = "customer"
    EMPLOYEE = "employee"
