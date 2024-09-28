from src.abstract_report import abstract_report
from src.errors.error_utils import error_proxy, operation_exception, argument_exception
from src.abstract_reference import abstract_reference

class rtf_report(abstract_report):
    
    def create(self, storage_key: str):
        super().create(storage_key)

        items = self.data[storage_key]
        if items is None:
            raise operation_exception("Error data")
        
        if len(items) == 0:
            raise operation_exception("Data empty")

        result = []
        
        # Начало RTF документа
        result.append(r"{\rtf1\ansi\deff0")
        
        # Заголовок
        result.append(r"{\b\fs24 " + storage_key + r"}\par")
        
        # Таблица
        result.append(r"\trowd\trgaph100\trleft-100")
        
        # Шапка таблицы
        for field in self.fields:
            result.append(rf"{{\b {field}\cell}}")  # Используем сырую строку с префиксом r
        result.append(r"\row")
        
        # Данные таблицы
        for item in items:
            for field in self.fields:
                attribute = getattr(item.__class__, field)
                if isinstance(attribute, property):
                    value = getattr(item, field)
                    if isinstance(value, (list, dict)) or value is None:
                        value = ""
                    
                    result.append(rf"{value}\cell")  # Используем сырой формат
            result.append(r"\row")
        
        # Закрытие RTF документа
        result.append(r"}")
        
        return "\n".join(result)