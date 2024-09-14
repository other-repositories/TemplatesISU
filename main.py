from settings_manager import settings_manager

s = settings_manager()
print(s.convert({ "organization_name" : "123", "inn": "3466"}).__dict__)

