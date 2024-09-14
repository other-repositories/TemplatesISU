import json
from datetime import datetime

class error_proxy_item:
    __error_text = ""

    @property
    def error(self):
        return self.__error_text
    
    @error.setter
    def error(self, value: str):
        if value == "":
            raise Exception("Invalid args!")
            
        self.__error_text = value
        
    @classmethod
    def set_error(self, exception: Exception):     
        if exception  is None:
            self.__error_text = ""
            return
            
        self.__error_text = f"Error! {str(exception)}"    
            

class error_proxy(Exception):
    __error : error_proxy_item = error_proxy_item()
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__error.set_error(self)

    # Validate information
    @staticmethod
    def check( value, type_, len_= None):
        if value is None:
            raise argument_exception(f"Empty arg")

        if not isinstance(value, type_):
            raise argument_exception(f"Incorrect Type")

        if len_ is not None and len(str(value).strip()) >= len_:
            raise argument_exception(f"Incorrect len {len_}")

        return True    

    @property    
    def error(self):
        return self.__error    

class argument_exception(error_proxy):
    pass     
    
class operation_exception(error_proxy):
    pass