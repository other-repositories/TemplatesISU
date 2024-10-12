from src.start_service import start_service
from src.settings_manager import settings_manager
from src.report_factory import report_factory
import json
from src.common import common
from flask import Flask, jsonify
from flasgger import Swagger
from src.errors.error_utils import error_proxy
# Пример вложенной модели
from src.dto_model import FilterDTO, FilterPrototype, FilterType

app = Flask(__name__)
Swagger(app)

app.config['JSON_AS_ASCII'] = False

manager = settings_manager()
start = start_service(manager.current_settings)
factory = report_factory(manager.current_settings)

def process_report_data(type, format_type):
    try:
        manager.current_settings.report_mode = format_type
        report = factory.create(None, start.get_storage().get_data())

        out = ''
        data = report.create(type)
        i = 0
        if format_type == "json":
            out += "["
            for elem in data:
                parsed_data = json.loads(elem)
                corrected_data = common.prepare_json_out(parsed_data)
                out += json.dumps(corrected_data, ensure_ascii=False, indent=4)
                if i != len(data) - 1:
                    i += 1
                    out += ","
            out += "]"
        else:
            out += f'"{data}"'

        return out

    except Exception as ex:
        return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)


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
    try:
        formats_list = [format.value for format in manager.current_settings.ConvertTypes]
        return jsonify(formats_list)
    except Exception as ex:
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
    try:
        return process_report_data("recipes", convert_type)
    except Exception as ex:
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
    try:
        return process_report_data("nomenclatures", convert_type)
    except Exception as ex:
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
    try:
        return process_report_data("groups", convert_type)
    except Exception as ex:
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
    try:
        return process_report_data("units", convert_type)
    except Exception as ex:
        return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)


@app.route("/api/dto/<dto_model>/<convert_type>/<model_type>/<name>/<unique_code>", methods=["GET"])
def dto(dto_model, convert_type, model_type, name, unique_code):
    """
    Применить фильтр DTO к данным
    ---
    parameters:
      - in: path
        name: dto_model
        required: true
        schema:
          type: string
        description: Тип DTO модели для фильтрации (например, "equals" или "like")
      - in: path
        name: convert_type
        required: true
        schema:
          type: string
        description: Формат отчета (например, "json" или "csv")
      - in: path
        name: model_type
        required: true
        schema:
          type: string
        description: Тип модели, к которой применяется фильтрация (например, "nomenclature" или "group")
      - in: path
        name: name
        required: true
        schema:
          type: string
        description: Наименование для фильтрации
      - in: path
        name: unique_code
        required: true
        schema:
          type: string
        description: Уникальный код для фильтрации
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

if __name__ == "__main__":
    # Загрузка начальных данных
    with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
        start.create(json.load(file))

    app.run(host="0.0.0.0", port=8080, debug=True)
