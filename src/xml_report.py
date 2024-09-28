from src.abstract_report import abstract_report
from src.errors.error_utils import error_proxy, operation_exception, argument_exception
from src.abstract_reference import abstract_reference
from src.models.receipt_model import receipt_model

import uuid
import xml.etree.ElementTree as ET

class xml_report(abstract_report):

    _maps = {}
    
    def uuid_convertor(self, field, object: uuid.UUID):
        element = ET.Element(field)
        element.text = object.hex
        return element
    
    def basic_convertor(self, field: str, object):
        element = ET.Element(field)
        element.text = str(object)
        return element
    
    def reference_convertor(self,field: str, object):
        factory = xml_report({"temp": object})
        return factory.create("temp")

    def __init__(self, data = None) -> None:
        super().__init__(data)
        self._maps[int] = self.basic_convertor
        self._maps[float] = self.basic_convertor
        self._maps[str] = self.basic_convertor
        self._maps[bool] = self.basic_convertor
        self._maps[uuid.UUID] = self.uuid_convertor
        for inheritor in abstract_reference.__subclasses__():
            self._maps[inheritor] = self.reference_convertor

    def create(self, storage_key: str):
        items = self.data[storage_key]

        result = self.__serialize_list("data", items)
        if result is not None:
            return ET.tostring(result, encoding="unicode")

        root = ET.Element("root")
        fields = abstract_reference.create_fields(items)

        for field in fields:
            attribute = getattr(items.__class__, field)
            if isinstance(attribute, property):
                value = getattr(items, field)
                element = self.__serialize_list(field, value)
                if element is None:
                    element = self.__serialize_item(field, value)
                if isinstance(element, str):
                    # Если элемент строка, создаем XML элемент
                    new_element = ET.Element(field)
                    new_element.text = element
                    root.append(new_element)
                else:
                    root.append(element)

        return ET.tostring(root, encoding="unicode")

    def __serialize_list(self, field: str, source):
        error_proxy.check(field, str)
        if isinstance(source, list):
            parent = ET.Element(field)
            for item in source:
                child = self.__serialize_item(field, item)
                if isinstance(child, str):
                    new_element = ET.Element(field)
                    new_element.text = child
                    parent.append(new_element)
                else:
                    parent.append(child)
            return parent

        if isinstance(source, dict):
            parent = ET.Element(field)
            for key, value in source.items():
                child = self.__serialize_item(key, value)
                if isinstance(child, str):
                    new_element = ET.Element(key)
                    new_element.text = child
                    parent.append(new_element)
                else:
                    parent.append(child)
            return parent

    def __serialize_item(self, field: str, source):
        error_proxy.check(field, str)
        if source is None:
            element = ET.Element(field)
            element.text = "None"
            return element

        if isinstance(source, (list, dict)):
            return self.__serialize_list(field, source)

        if type(source) not in self._maps.keys():
            raise operation_exception(f"Не возможно подобрать конвертор для типа {type(source)}")

        convertor = self._maps[type(source)]
        element = convertor(field, source)

        # Если конвертор вернул строку, обрабатываем это
        if isinstance(element, str):
            new_element = ET.Element(field)
            new_element.text = element
            return new_element

        return element
