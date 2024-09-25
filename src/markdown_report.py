from src.abstract_report import abstract_report
from src.errors.error_utils import error_proxy, operation_exception, argument_exception

class markdown_report(abstract_report):
    
      def create(self, storage_key: str):
        super().create(storage_key)
        result = []

        # Исходные данные
        items = self.data[ storage_key ]
        if items == None:
            raise operation_exception("Невозможно сформировать данные. Данные не заполнены!")
        
        
        if len(items) == 0:
            raise operation_exception("Невозможно сформировать данные. Нет данных!")
        
        # Заголовок
        result.append(f"# {storage_key}")
        
        # Шапка таблицы
        header = ""
        line = ""
        for field in self.fields:
            header += f"|{field}"
            line += "|--"
        
        result.append(f"{header}|")
        result.append(f"{line}|")
        
        # Данные
        for item in items:
            row = ""
            for field in self.fields:
                attribute = getattr(item.__class__, field)
                if isinstance(attribute, property):
                    value = getattr(item, field)
                    if isinstance(value, (list, dict)) or value is None:
                        value = ""
                        
                    row +=f"|{value}"  
                
            result.append(f"{row}|")
            
        return "\n".join(result)        
    
     
    