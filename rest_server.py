from src.start_service import start_service
from src.settings_manager import settings_manager
from src.report_factory import report_factory
import json
from src.common import common
from flask import Flask, jsonify, request
from flasgger import Swagger
from src.errors.error_utils import error_proxy
# Пример вложенной модели
from src.dto_model import FilterDTO, FilterPrototype, FilterType
from datetime import datetime
from src.storage import storage_repository
app = Flask(__name__)
Swagger(app)

from src.process_factory import process_factory
from src.storage_prototype import storage_prototype
from src.models.storage_row_turn_model import storage_row_turn_model
from src.models.storage_model import storage_model
from src.models.range_model import range_model as unit_model

from src.models.nomenclature_model import nomenclature_model
from src.chain.storage_service import storage_service

from src.chain.nomenclature_service import nomenclature_service

app.config['JSON_AS_ASCII'] = False

manager = settings_manager()
start = start_service(manager.current_settings)
factory = report_factory(manager.current_settings)
service_nom = None

from src.logger import CustomLogger 

@app.route("/api/report_types", methods=["GET"])
def report_types():
    """
    Получить список доступных типов отчетов
    ---
    responses:
      200:
        description: Список доступных форматов
        content:
          application/json:
            schema:
              type: array
              items:
                type: string
      500:
        description: Ошибка при формировании отчета
    """
    CustomLogger.info(f"Получен запрос на список типов отчетов: {request.url}")
    try:
        formats_list = [format.value for format in manager.current_settings.ConvertTypes]
        CustomLogger.info(f"Список доступных форматов: {formats_list}")
        return jsonify(formats_list)
    except Exception as ex:
        CustomLogger.error(f"Ошибка при формировании списка форматов: {ex}")
        return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)

@app.route("/api/recipes/<convert_type>", methods=["GET"])
def get_recipes(convert_type):
    """
    Получить список рецептов
    ---
    parameters:
      - in: path
        name: convert_type
        required: true
        schema:
          type: string
        description: Формат отчета (например, "json" или "csv")
    responses:
      200:
        description: Список рецептов
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    CustomLogger.info(f"Получен запрос на список рецептов. Формат: {convert_type}, URL: {request.url}")
    try:
        result = common.process_report_data("recipes", convert_type, manager, factory, start)
        CustomLogger.info("Список рецептов успешно сформирован.")
        return result
    except Exception as ex:
        CustomLogger.error(f"Ошибка при формировании списка рецептов: {ex}")
        return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)


@app.route("/api/nomenclatures/<convert_type>", methods=["GET"])
def get_nomenclatures(convert_type):
    """
    Получить список номенклатур
    ---
    parameters:
      - in: path
        name: convert_type
        required: true
        schema:
          type: string
        description: Формат отчета (например, "json" или "csv")
    responses:
      200:
        description: Список номенклатур
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    CustomLogger.info(f"Получен запрос на список номенклатур. Формат: {convert_type}, URL: {request.url}")
    try:
        result = common.process_report_data("nomenclatures", convert_type, manager, factory, start)
        CustomLogger.info("Список номенклатур успешно сформирован.")
        return result
    except Exception as ex:
        CustomLogger.error(f"Ошибка при формировании списка номенклатур: {ex}")
        return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)


@app.route("/api/groups/<convert_type>", methods=["GET"])
def get_groups(convert_type):
    """
    Получить список групп
    ---
    parameters:
      - in: path
        name: convert_type
        required: true
        schema:
          type: string
        description: Формат отчета (например, "json" или "csv")
    responses:
      200:
        description: Список групп
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    CustomLogger.info(f"Получен запрос на список групп. Формат: {convert_type}, URL: {request.url}")
    try:
        result = common.process_report_data("groups", convert_type, manager, factory, start)
        CustomLogger.info("Список групп успешно сформирован.")
        return result
    except Exception as ex:
        CustomLogger.error(f"Ошибка при формировании списка групп: {ex}")
        return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)


@app.route("/api/units/<convert_type>", methods=["GET"])
def get_units(convert_type):
    """
    Получить список единиц измерения
    ---
    parameters:
      - in: path
        name: convert_type
        required: true
        schema:
          type: string
        description: Формат отчета (например, "json" или "csv")
    responses:
      200:
        description: Список единиц измерения
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    CustomLogger.info(f"Получен запрос на список единиц измерения. Формат: {convert_type}, URL: {request.url}")
    try:
        result = common.process_report_data("units", convert_type, manager, factory, start)
        CustomLogger.info("Список единиц измерения успешно сформирован.")
        return result
    except Exception as ex:
        CustomLogger.error(f"Ошибка при формировании списка единиц измерения: {ex}")
        return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)

@app.route("/api/dto/<model_type>/<dto_model>", methods=["GET"])
@app.route("/api/dto/<model_type>/<dto_model>/<convert_type>", methods=["GET"])
def dto(model_type, dto_model, convert_type="json"):
    """
    Применить фильтр DTO к данным
    ---
    parameters:
      - in: path
        name: model_type
        required: true
        schema:
          type: string
        description: Тип модели, к которой применяется фильтрация (например, "nomenclature" или "group")
      - in: path
        name: dto_model
        required: true
        schema:
          type: string
        description: Тип DTO модели для фильтрации (например, "equals" или "like")
      - in: path
        name: convert_type
        required: false
        schema:
          type: string
        description: Формат отчета (например, "json" или "csv")
    responses:
      200:
        description: Отфильтрованные данные
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
      500:
        description: Ошибка при формировании отчета
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Описание ошибки
    """
    try:
        name = request.args.get('name')
        unique_code = request.args.get('unique_code') 

        manager.current_settings.report_mode = convert_type
        report = factory.create(None, start.get_storage().get_data())

        out = ''
        data = report.create(model_type)

        filter_type=FilterType.LIKE

        if(dto_model == 'equals'):
            filter_type=FilterType.EQUALS

        filter_dto = FilterDTO(filter_type=filter_type, name=name,unique_code=unique_code )

        # Применяем фильтр
        filter_prototype = FilterPrototype()
        if(isinstance(data, list)):
            filtered_units = filter_prototype.filter(data, filter_dto)
        else:
            filtered_units = filter_prototype.filter([data], filter_dto)

        i = 0
        if convert_type == "json":
            out += "["
            for elem in filtered_units:
                parsed_data = json.loads(elem)
                corrected_data = common.prepare_json_out(parsed_data)
                out += json.dumps(corrected_data, ensure_ascii=False, indent=4)
                if i != len(filtered_units) - 1:
                    i += 1
                    out += ","
            out += "]"
        else:
            out += f'"{filtered_units}"'
        return out

    except Exception as ex:
        return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)

@app.route("/api/storage/turns", methods = ["GET"] )
def get_turns():
    args = request.args
    if "start_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!")
        
    if "stop_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!")
    
    start_date = datetime.strptime(args["start_period"], "%Y-%m-%d")
    stop_date = datetime.strptime(args["stop_period"], "%Y-%m-%d")

    transactions = start.get_storage().get_data()["storage_row_model"] 
    data = storage_service( transactions ).create_turns( start_date, stop_date )   

    factory = report_factory(manager.current_settings)
    manager.current_settings.report_mode = "json"
    report = factory.create(None, {"storage_row_model": data})

    return common.prepare_array_json()

@app.route("/api/block_period", methods=["GET"])
def get_block_period():
    result = [manager.current_settings.block_period.strftime('%Y-%m-%d')]
    return result

@app.route("/api/set_block_period", methods=["POST"])
def set_block_period():
    args = request.args
    if "period" in args.keys():
        try:
            period = datetime.strptime(args["period"], "%Y-%m-%d")
            manager.current_settings.block_period = period
        except:
           return error_proxy.create_error_response(app, "Некорректно перпеданы параметры: period", 400) 
    return ""

@app.route("/api/set_block_period", methods=["POST"])
def set_block_period():
    args = request.args
    if "period" in args.keys():
        try:
            period = datetime.strptime(args["period"], "%Y-%m-%d")
            manager.current_settings.block_period = period
        except:
           return error_proxy.create_error_response(app, "Некорректно перпеданы параметры: period", 400) 
    return ""

@app.route("/api/insert_nomenclature", methods=["PUT"])
def insert_nomenclature():
    body = request.json
    CustomLogger.info(f"Получен запрос на добавление номенклатуры. Тело запроса: {body}")
    try:
        result = service_nom.insert_nomenclature(body)
        CustomLogger.info(f"Номенклатура успешно добавлена: {body}")
        return result
    except Exception as ex:
        CustomLogger.error(f"Ошибка при добавлении номенклатуры: {ex}")
        return error_proxy.create_error_response(app, f"Ошибка при добавлении номенклатуры {ex}", 500)


@app.route("/api/update_nomenclature", methods=["PATCH"])
def update_nomenclature():
    body = request.json
    CustomLogger.info(f"Получен запрос на обновление номенклатуры. Тело запроса: {body}")
    try:
        result = service_nom.update_nomenclature(body)
        CustomLogger.info(f"Номенклатура успешно обновлена: {body}")
        return result
    except Exception as ex:
        CustomLogger.error(f"Ошибка при обновлении номенклатуры: {ex}")
        return error_proxy.create_error_response(app, f"Ошибка при обновлении номенклатуры {ex}", 500)


def trigger_delete(json_text):
    for item in start.get_storage().get_data()["recipes"]:
        for receipt in item.receipts_list:
            if(receipt.nomenclature.unique_code in json_text):
                return False 
    return True
                 
@app.route("/api/delete_nomenclature", methods=["POST"])
def delete_nomenclature():
    body = request.json
    CustomLogger.info(f"Получен запрос на удаление номенклатуры. Тело запроса: {body}")
    try:
        result = service_nom.delete_nomenclature(body)
        CustomLogger.info(f"Номенклатура успешно удалена: {body}")
        return result
    except Exception as ex:
        CustomLogger.error(f"Ошибка при удалении номенклатуры: {ex}")
        return error_proxy.create_error_response(app, f"Ошибка при удалении номенклатуры {ex}", 500)


@app.route("/api/get_nomenclature", methods=["GET"])
def get_nomenclature():
    body = request.json 
    return service_nom.get_nomenclature(body)        

@app.route("/api/report/<storage_key>", methods = ["GET"])
def get_report(storage_key: str):
    if storage_key == "":
        return error_proxy.create_error_response(app, f"Некорректный передан запрос! Необходимо передать: /api/report/<storage_key>.", 400)
    
    try:
        result = common.process_report_data(storage_key, "json", manager, factory, start) 
        return result
    except Exception as ex:
        return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)

@app.route("/api/save_storage", methods=["POST"])
def save_storage_nomenclature():
    start.get_storage().save()
    manager.current_settings.init_storage()

@app.route("/api/load_storage", methods=["POST"])
def load_storage_nomenclature():
    start.get_storage().load()

if __name__ == "__main__":
    # Загрузка начальных данных
    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    service_nom = nomenclature_service(start.get_storage().get_data()["nomenclatures"])
    service_nom.set_trigger_before_delete(trigger_delete)

    app.run(host="0.0.0.0", port=8080, debug=True)
