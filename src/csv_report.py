from src.abstract_report import abstract_report
from src.errors.error_utils import error_proxy, operation_exception, argument_exception


class csv_report(abstract_report):

    def create(self, storage_key: list):
        super().create(storage_key)
        result = ""
        delimetr = ";"

        # Исходные данные
        items = self.data[ storage_key ]
        if items == None:
            raise operation_exception("Error data")
        
        if len(items) == 0:
            raise operation_exception("Data empty")
        
        # Заголовок 
        header = delimetr.join(self.fields)
        result += f"{header}\n"
        
        # Данные
        for item in items:
            row = ""
            for field in self.fields:
                attribute = getattr(item.__class__, field)
                if isinstance(attribute, property):
                    value = getattr(item, field)
                    if isinstance(value, (list, dict)) or value is None:
                        value = ""
                        
                    row +=f"{value}{delimetr}"
                
            result += f"{row[:-1]}\n"
            
        
        # Результат csv
        return result
