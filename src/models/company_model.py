from  src.abstract_reference import abstract_reference
from  src.errors.error_utils import error_proxy, operation_exception, argument_exception
from  src.settings import settings

class company_model(abstract_reference):
    def __init__(self, name,  sett: settings, bill = None):
        super().__init__(name)
        self.inn = sett.inn
        self.bik = sett.bik
        self.ownership_type = sett.ownership_type
        if(bill is not None):
            self.bill = bill

    @property
    def inn(self):
        return self._inn

    @inn.setter
    def inn(self, value):
        if len(value) != 12:
            raise argument_exception("ИНН должен содержать ровно 12 символов.")
        self._inn = value

    @property
    def bik(self):
        return self._bik

    @bik.setter
    def bik(self, value):
        if len(value) != 9:
            raise argument_exception("БИК должен содержать ровно 9 символов.")
        self._bik = value

    @property
    def bill(self):
        return self._bill

    @bill.setter
    def bill(self, value):
        self._bill = value

    @property
    def ownership_type(self):
        return self._ownership_type

    @ownership_type.setter
    def ownership_type(self, value):
        if len(value) != 5:
            raise argument_exception("Вид собственности должен содержать ровно 5 символов.")
        self._ownership_type = value
