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
from src.logger import CustomLogger  # Импорт статического логгера

import json


class nomenclature_service(service):
    trigger_before_delete = None  # pattern strategy
    json_deser = json_deserializer()
    json_rep = json_report()

    def __init__(self, data: list, trigger_before_delete=None) -> None:
        super().__init__(data)
        self.trigger_before = trigger_before_delete
        CustomLogger.info(f"Инициализация nomenclature_service с данными: {data}")

    def set_trigger_before_delete(self, foo):
        CustomLogger.info("Установка триггера перед удалением.")
        self.trigger_before_delete = foo

    def insert_nomenclature(self, object: json) -> list:
        CustomLogger.info(f"Вставка номенклатуры с объектом: {object}")
        try:
            nomenclature_model_new = self.json_deser.deserialize_model(object)
            self.data.append(nomenclature_model_new)
            CustomLogger.info(f"Номенклатура успешно добавлена: {nomenclature_model_new}")
        except Exception as ex:
            CustomLogger.error(f"Ошибка при вставке номенклатуры: {ex}")
            return ex

        return ""

    def update_nomenclature(self, object: json) -> list:
        CustomLogger.info(f"Обновление номенклатуры с объектом.")
        try:
            for i in range(len(self.data)):
                item = self.data[i]
                nomenclature_model_new = self.json_deser.deserialize_model(object)
                if item.unique_code == nomenclature_model_new["unique_code"]:
                    self.data[i] = nomenclature_model_new
                    CustomLogger.info(f"Номенклатура под индексом {i} заменена другой.")
                    return ""
        except Exception as ex:
            CustomLogger.error(f"Ошибка при обновлении номенклатуры: {ex}")
            return ex

        CustomLogger.warning("Номенклатура для обновления не найдена.")
        return "Error nomenclature not founded"

    def delete_nomenclature(self, object_text: json) -> list:
        CustomLogger.info(f"Удаление номенклатуры с объектом: {object_text}")
        try:
            if self.trigger_before_delete:
                if not self.trigger_before_delete(object_text):
                    CustomLogger.error("Триггер перед удалением вернул False.")
                    return "Error Trigger return False"

            for i in range(len(self.data)):
                item = self.data[i]
                nomenclature_model_new = self.json_deser.deserialize_model(object_text)
                if item.unique_code == nomenclature_model_new["unique_code"]:
                    self.data.pop(i)
                    CustomLogger.info(f"Номенклатура успешно удалена: {nomenclature_model_new}")
                    return ""
        except Exception as ex:
            CustomLogger.error(f"Ошибка при удалении номенклатуры: {ex}")
            return ex

        CustomLogger.warning("Номенклатура для удаления не найдена.")
        return "Error nomenclature not founded"

    def get_nomenclature(self, object_text: json) -> list:
        CustomLogger.info(f"Получение номенклатуры с объектом: {object_text}")
        try:
            for i in range(len(self.data)):
                item = self.data[i]
                nomenclature_model_new = self.json_deser.deserialize_model(object_text)
                if item.unique_code == nomenclature_model_new["unique_code"]:
                    result = self.json_rep.create(item)
                    CustomLogger.info(f"Номенклатура найдена: {result}")
                    return result
        except Exception as ex:
            CustomLogger.error(f"Ошибка при получении номенклатуры: {ex}")
            return nomenclature_model()

        CustomLogger.warning("Номенклатура не найдена.")
        return nomenclature_model()
