from  src.errors.error_utils import error_proxy, operation_exception, argument_exception
from enum import Enum

class ConvertTypes(Enum):
    XML = "xml",
    CSV = "csv",
    JSON = "json",
    RTF = "rtf",
    MD = "markdown"

class settings:

    _mode = "csv"

    def __init__(self):
        self.inn = "0" * 12
        self.account_number = "0" * 11
        self.correspondent_account = "0" * 11
        self.bik = "0" * 9
        self.organization_name = ""
        self.ownership_type = "0" * 5

    @property
    def inn(self):
        return self._inn

    @inn.setter
    def inn(self, value):
        if len(value) != 12:
            raise argument_exception("ИНН должен содержать ровно 12 символов.")
        self._inn = value

    @property
    def account_number(self):
        return self._account_number

    @account_number.setter
    def account_number(self, value):
        if len(value) != 11:
            raise argument_exception("Счет должен содержать ровно 11 символов.")
        self._account_number = value

    @property
    def correspondent_account(self):
        return self._correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value):
        if len(value) != 11:
            raise argument_exception("Корреспондентский счет должен содержать ровно 11 символов.")
        self._correspondent_account = value

    @property
    def bik(self):
        return self._bik

    @bik.setter
    def bik(self, value):
        if len(value) != 9:
            raise argument_exception("БИК должен содержать ровно 9 символов.")
        self._bik = value

    @property
    def organization_name(self):
        return self._organization_name

    @organization_name.setter
    def organization_name(self, value):
        self._organization_name = value

    @property
    def ownership_type(self):
        return self._ownership_type

    @ownership_type.setter
    def ownership_type(self, value):
        if len(value) != 5:
            raise argument_exception("Вид собственности должен содержать ровно 5 символов.")
        self._ownership_type = value

    @property
    def report_mode(self):
        return self._mode
    
    @report_mode.setter
    def report_mode(self, value: str):
        error_proxy.check(value, str)
        
        self._mode = value
