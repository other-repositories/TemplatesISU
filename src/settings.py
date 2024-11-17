from  src.errors.error_utils import error_proxy, operation_exception, argument_exception
from enum import Enum
from src.markdown_report import markdown_report
from src.csv_report import csv_report
from src.json_report import json_report
from src.xml_report import xml_report
from src.rtf_report import rtf_report
from datetime import datetime
import json

class settings:

    class ConvertTypes(Enum):
        XML = "xml"
        CSV = "csv"
        JSON = "json"
        RTF = "rtf"
        MD = "markdown"

    __file_name = "settings.json"
    _mode = ConvertTypes.CSV.value
    _block_period : datetime = datetime.strptime("1999-12-12", "%Y-%m-%d") #datetime.now()
    _is_first_start = False
    _maps = {}

    def __init__(self):
        self.inn = "0" * 12
        self.account_number = "0" * 11
        self.correspondent_account = "0" * 11
        self.bik = "0" * 9
        self.organization_name = ""
        self.ownership_type = "0" * 5
        self._maps[self.ConvertTypes.CSV.value]  = csv_report
        self._maps[self.ConvertTypes.MD.value] = markdown_report
        self._maps[self.ConvertTypes.JSON.value] = json_report
        self._maps[self.ConvertTypes.XML.value] = xml_report
        self._maps[self.ConvertTypes.RTF.value] = rtf_report
        #self.open()

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

    def get_convert_types(self):
        return self._maps

    @property
    def block_period(self):
        return self._block_period

    @block_period.setter
    def block_period(self, value):
        legacy_period = self._block_period
        
        if isinstance(value, datetime):
            self._block_period = value
            return

        if isinstance(value, str):
            try:
               self._block_period = datetime.strptime(value, "%Y-%m-%d")    
            except Exception as ex:
                raise argument_exception(f"Невозможно сконвертировать сроку в дату! {ex}")
        else:
            raise argument_exception("Некорректно переданы параметры!")
        
        self.save()

    def init_storage(self):
        self._is_first_start = True

    def get_var_settings(self):
        return {"block_period": self._block_period.strftime("%Y-%m-%d"),"is_first_start":self._is_first_start}
    
    def set_var_settings(self, data):
            self._block_period = datetime.strptime(data["block_period"], "%Y-%m-%d")
            self._is_first_start = data["is_first_start"]       