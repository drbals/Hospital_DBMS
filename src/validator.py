import re
from datetime import datetime
from config import DOCTOR_MASTER_PASSWORD

class Validator:
    @staticmethod
    def validate_dob(dob_str):
        try:
            datetime.strptime(dob_str, "%Y-%m-%d")
            return True, ""
        except ValueError:
            return False, "Date of Birth must be in YYYY-MM-DD format."

    @staticmethod
    def validate_gender(gender):
        if gender == "Select":
            return False, "Please select a gender."
        return True, ""

    @staticmethod
    def validate_contact(contact):
        if not contact.isdigit() or len(contact) != 10:
            return False, "Contact number must be exactly 10 digits."
        return True, ""

    @staticmethod
    def validate_email(email):
        pattern = r"@.*\.com$"
        if not re.search(pattern, email):
            return False, "Email must end with '@domain.com'."
        return True, ""

    @staticmethod
    def validate_password(password):
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."
        return True, ""
    
    @staticmethod
    def validate_doctor_masterpwd(masterpwd):
        if masterpwd != DOCTOR_MASTER_PASSWORD:
            return False, "Invalid master password!"
        return True, ""

    @staticmethod
    def validate_doc_salary(salary):
        if not salary.isdigit() or int(salary) <= 0:
            return False, "Salary must be a positive number."
        return True, ""
    
    @staticmethod
    def validate_dept_number(dept_number):
        if not dept_number.isdigit() or int(dept_number) <= 0:
            return False, "Department number must be a positive number."
        return True, ""