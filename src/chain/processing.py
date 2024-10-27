import abc
from src.errors.error_utils import error_proxy, argument_exception, operation_exception

#
# Абстрактный класс для наследования.
# Используется для реализации различных процессов обработки данных по складским транзакциям
#
class processing(error_proxy):
    
    @abc.abstractmethod
    def process(self, transactions: list) -> list:
        if transactions == None:
            raise argument_exception("Некорректно передан параметр!")
        
        if len(transactions) == 0:
            raise argument_exception("Некорректно передан параметр!")
        
        self.clear()