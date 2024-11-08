from src.errors.error_utils import error_proxy, argument_exception, operation_exception
from datetime import datetime
from src.models.nomenclature_model import nomenclature_model
from src.chain.service import service 
from src.process_factory import process_factory
from src.storage_prototype import storage_prototype
from src.models.receipt_model import receipt_model
from src.deserializer_json import json_deserializer
from src.json_report import json_report

from datetime import datetime

import json

class nomenclature_service(service):
    
    trigger_before_delete = None #pattern strategy
    json_deser = json_deserializer()
    json_rep = json_report()

    def __init__(self, data : list, trigger_before_delete=None) -> None:
        super().__init__(data)
        self.trigger_before = trigger_before_delete
    
    def set_trigger_before_delete(self, foo):
        self.trigger_before_delete = foo

    def insert_nomenclature(self, object: json) -> list:
        try:
            nomenclature_model_new = self.json_deser.deserialize_model(object)
            self.data.append(nomenclature_model_new)
        except Exception as ex: 
            return ex
        
        return ""
         
    def update_nomenclature(self, object_text: json ) -> list:
        for i in range(self.data):
            item = self.data[i]
            nomenclature_model_new = self.json_deser.deserialize_model(object_text)
            if item.unique_code == nomenclature_model_new["unique_code"]:
                try:
                    self.data[i] = nomenclature_model_new
                    return ""
                except Exception as ex: 
                    return ex
        return "Error nomenclature not founded"

    def delete_nomenclature(self, object_text: json ) -> list:
        if self.trigger_before_delete:
            if(not self.trigger_before_delete(object_text)):
                return "Error Trggier return False"
            
        for i in range(self.data):
            item = self.data[i]
            nomenclature_model_new = self.json_deser.deserialize_model(object_text)
            if item.unique_code == nomenclature_model_new["unique_code"]:
                self.data.pop(i)
                return ""
        return "Error nomenclature not founded"
    
    def get_nomenclature(self, object_text: json ) -> list:
        for i in range(self.data):
            item = self.data[i]
            nomenclature_model_new = self.json_deser.deserialize_model(object_text)
            if item.unique_code == nomenclature_model_new["unique_code"]:
                return self.json_rep.create(item)
        return nomenclature_model()
