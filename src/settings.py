        
"""
Настройки
"""
class settings:
    def __init__(self):
        self.inn = "123123123123"
        self.account_number = "12312312312"
        self.correspondent_account = "12312312312"
        self.bik = "123123123"
        self.organization_name = ""
        self.ownership_type = "12312"

    @property
    def inn(self):
        return self._inn

    @inn.setter
    def inn(self, value):
        if len(value) != 12:
            raise ValueError("ИНН должен содержать ровно 12 символов.")
        self._inn = value

    @property
    def account_number(self):
        return self._account_number

    @account_number.setter
    def account_number(self, value):
        if len(value) != 11:
            raise ValueError("Счет должен содержать ровно 11 символов.")
        self._account_number = value

    @property
    def correspondent_account(self):
        return self._correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value):
        if len(value) != 11:
            raise ValueError("Корреспондентский счет должен содержать ровно 11 символов.")
        self._correspondent_account = value

    @property
    def bik(self):
        return self._bik

    @bik.setter
    def bik(self, value):
        if len(value) != 9:
            raise ValueError("БИК должен содержать ровно 9 символов.")
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
            raise ValueError("Вид собственности должен содержать ровно 5 символов.")
        self._ownership_type = value

