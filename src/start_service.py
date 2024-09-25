from src.settings import settings
from src.errors.error_utils import error_proxy, argument_exception, operation_exception

from src.models.range_model import range_model
from src.models.nomenclature_model import nomenclature_model
from src.models.nom_group_model import nom_group_model
from src.abstract_reference import abstract_reference
from src.models.storage_model import storage_model
from src.models.receipt_model import receipt_model
from src.storage import storage_repository

import json

class start_service:
    __options: storage_repository = None
    __storage = None

    def __init__(self, _options: settings = None, _storage: storage_repository = None) -> None:
        self.__options = _options
        if(_storage == None):
            self.__storage = storage_repository()
        else:
            self.__storage = _storage
    
    @staticmethod
    def create_units() -> list:
        items = []
        items.append( range_model.create_gram() )
        items.append( range_model.create_killogram() )
        items.append( range_model.create_ting() )
        return items
    
    @staticmethod
    def create_nomenclatures() -> list:
        group = nom_group_model.create_group()
        items = [ {"Пшеничная мука": "киллограмм"}, 
                  {"Сахар":"киллограмм"}, 
                  {"Сливочное масло" : "киллограмм"}, 
                  {"Яйца": "штука"}, 
                  {"Ванилин": "грамм"}, 
                  {"Куринное филе": "киллограмм"}, 
                  {"Салат Романо": "грамм"},
                  {"Сыр Пармезан" : "киллограмм"}, 
                  {"Чеснок": "киллограмм"} ]
        
        units = abstract_reference.transform_to_dict(start_service.create_units())
        
        result = []
        for position in items:

            tuple = list(position.items())[0]
            if len(tuple) < 2:
                raise operation_exception("Incorrect tuple!")
            
            name   = tuple[0]
            unit_name = tuple[1]

            if not unit_name in units.keys():
                raise operation_exception(f"Невозможно найти в списке указанную единицу измерения {unit_name}!")
            
            item = nomenclature_model( "",name, group, units[unit_name])
            result.append(item)
          
        return result
      
    @staticmethod      
    def create_groups() -> list:
        items = []
        items.append( nom_group_model.create_group())
        return items         
    
    def get_storage(self):
        return self.__storage

    @staticmethod
    def create_receipt(name, items, extra, full_desc, _data_nom: list = None) -> list:    
        if _data_nom is None:
            data = start_service.create_nomenclatures()
        else:
            data = _data_nom
            
        if len(data) == 0:
            raise argument_exception("List empty")        
        
        item = receipt_model.create_receipt(name, extra, items, data)
        item.full_desc.extend(full_desc)
        return item


    def create(self, receipt_dict) -> bool:    
        nomenclatures = start_service.create_nomenclatures()
        name = receipt_dict["title"]
        ingredients = [(ingredient["name"], int(ingredient["amount"].split()[0])) for ingredient in receipt_dict["ingredients"] if "amount" in ingredient]
        instructions = receipt_dict["instructions"]
        extra = f"Время приготовления: {receipt_dict['cooking_time']}"
        
        item = start_service.create_receipt(name,ingredients, extra, instructions, nomenclatures)
        self.__storage.add_recipe(item)

        start_service.create_units()
        start_service.create_groups()

        return True
             