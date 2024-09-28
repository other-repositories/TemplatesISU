from src.abstract_reference import abstract_reference
from src.models.receipt_model_unit import receipt_model_unit
from src.errors.error_utils import error_proxy, argument_exception, operation_exception
from src.models.nomenclature_model import nomenclature_model

class receipt_model(abstract_reference):
    _receipts_list = {}
    _full_desc: str = ""
    _extra_info: str = ""
    
    def __init__(self, name = None):
        super().__init__(name)
        self._receipts_list = {}
        self._full_desc = ""
            
    def add(self, row: receipt_model_unit):
        error_proxy.check(row, receipt_model_unit)
        self._receipts_list[row.name] = row
        
    def delete(self, name):
        if name in self._receipts_list.keys():
            self._receipts_list.pop(row.name)   
        
    @property    
    def full_desc(self) -> str:
        return self._full_desc
    
    @full_desc.setter   
    def full_desc(self, list):
        self._full_desc = str().join(list)

    @property
    def extra_info(self) -> str:
        return self._extra_info
    
    @extra_info.setter
    def extra_info(self, value: str):
        error_proxy.check(value, str)
        self._extra_info = value   
        
    @property            
    def receipts_list(self) -> list:
        return self._receipts_list    
    
    @receipts_list.setter
    def receipts_list(self) -> list:
        result = []
        for key in self._receipts_list.keys():
            result.append( self._receipts_list[key] )
        return result
    
    @staticmethod
    def create_receipt(name: str, extra_info: str, items: list, data: list):
        error_proxy.check(name, str)
        if len(items) == 0:
            raise argument_exception(f"List empty!")
        
        nomenclatures = abstract_reference.transform_to_dict(data)    
        receipt = receipt_model(name)
        if extra_info != "":
            receipt.extra_info = extra_info    
        
        for ingredient in items:
            
            if len(ingredient) != 2:
                raise operation_exception("ingredient error")
            
            nomenclature_name = ingredient[0]
            size = ingredient[1]        

            nomenclature = nomenclature_model.get( nomenclature_name, nomenclatures )

            if nomenclature.range.base_range is None:
                range = nomenclature.range
            else:
                range = nomenclature.range.base_range    
            
            row = receipt_model_unit()
            row.nomenclature = nomenclature
            row.size = size
            row.unit = range
            receipt.add(row)
        
        return receipt
    
    def get_receipt_details(self):
        details = {
            "title": self._name,
            "ingredients": []
        }
        
        for row in self._receipts_list.values():
            details["ingredients"].append({
                "name": row.nomenclature.name,
                "size": row.size,
                "unit": row.unit.name  
            })

        details["full_desc"] = self._full_desc

        details["extra"] = self._extra_info
        
        return details