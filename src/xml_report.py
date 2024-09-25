from src.abstract_report import abstract_report
from src.errors.error_utils import error_proxy, operation_exception, argument_exception
from src.abstract_reference import abstract_reference

class xml_report(abstract_report):
    
    def create(self, storage_key: str):
        super().create(storage_key)

        items = self.data[storage_key]
        if items is None:
            raise operation_exception("Error data")
        
        if len(items) == 0:
            raise operation_exception("Data empty")

        result = ['<?xml version="1.0" encoding="UTF-8"?>']
        result.append(f"<{storage_key}>")

        for item in items:
            result.append(self.__serialize_item(item))

        result.append(f"</{storage_key}>")
        
        return "\n".join(result)
    
    def __serialize_item(self, item):
        fields = self.fields
        result = [f"<item>"]
        
        for field in fields:
            attribute = getattr(item.__class__, field)
            if isinstance(attribute, property):
                value = getattr(item, field)
                if isinstance(value, (list, dict)) or value is None:
                    value = ""
                    
                result.append(f"<{field}>{value}</{field}>")
                
        result.append("</item>")
        
        return "\n".join(result)