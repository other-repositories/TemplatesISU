from src.errors.error_utils import error_proxy, argument_exception, operation_exception
from datetime import datetime
from src.models.nomenclature_model import nomenclature_model
from src.chain.service import service 
from src.process_factory import process_factory
from src.storage_prototype import storage_prototype
from src.models.receipt_model import receipt_model

from datetime import datetime

class storage_service(service):
    
    def __init__(self, data: list) -> None:
        super().__init__(data)
    
    def __build_turns(self, data: list) -> list:
        if len(data) == 0:
            raise argument_exception("Некорректно переданы параметры!")
        
        # Подобрать процессинг    
        key_turn = process_factory.turn_key()
        processing = process_factory().create( key_turn  )
    
        # Обороты
        turns =  processing().process( data )
        return turns

    def create_turns(self, start_period: datetime, stop_period:datetime ) -> list:
        error_proxy.check(start_period, datetime)
        error_proxy.check(stop_period, datetime)
        
        if start_period > stop_period:
            raise argument_exception("Некорректно переданы параметры!")
        
        block_period = self.settings.block_period
        print(block_period)
        # Фильтруем      
        prototype = storage_prototype(  self.data )  
        filter = prototype.filter_by_period( block_period, stop_period)
        
        # Рассчитанные обороты
        calculated_turns = self.__build_turns( filter. data )
        
        # Сформируем результат
        aggregate_key = process_factory.aggregate_key()
        processing = process_factory().create( aggregate_key  )
        return processing().process( calculated_turns )
         
  