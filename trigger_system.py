from src.models.nomenclature_model import nomenclature_model
from src.abstract_reference import abstract_reference
from src.start_service import start_service

#OBSERVER REALIZATION

class TriggerSystem:
    def __init__(self):
        self.__observers = set()

    def attach(self, observer):
        self._obbservers.add(observer)

    def detach(self, observer):
        self._obbservers.add(observer)
    
    def notify(model, self):
        is_error = False
        for observer in self.__observers:
            is_error = is_error or not(observer.trigger_call(model))
        return is_error

class TriggerBeforeDelete:
    start : start_service = None 

    def __init__(self, start : start_service):
        self.start = start
    def trigger_call(self, model): 
        for item in self.start.get_storage().get_data()["recipes"]:
            for receipt in item.receipts_list:
                if(receipt.nomenclature.unique_code in model.unique_code):
                    return False 
            return True
        