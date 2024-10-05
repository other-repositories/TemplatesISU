from src.start_service import start_service
from src.settings_manager import settings_manager
from src.report_factory import report_factory
import json 
from src.common import common
from flask import Flask
from flasgger import Swagger
from src.errors.error_utils import error_proxy, argument_exception, operation_exception


app = Flask(__name__)
Swagger(app)

app.config['JSON_AS_ASCII'] = False

manager = settings_manager()
manager.current_settings.report_mode = "json"
start = start_service( manager.current_settings )

@app.route("/api/report_types", methods = ["GET"])
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
        formats_json = json.dumps(formats_list, indent=4)
        return formats_json
    except Exception as ex:
        return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)
    
@app.route("/api/get_report/<format_type>", methods = ["GET"] )
def get_report(format_type: str):
    """
    Получить отчет в указанном формате
    ---
    parameters:
      - name: format_type
        in: path
        type: string
        required: true
        description: Формат отчета (например, json, csv и т.д.)
    responses:
      200:
        description: Отчет в указанном формате
        content:
          application/json:
            schema:
              type: object
              properties:
                recipes:
                  type: array
                  description: Список рецептов
                nomenclatures:
                  type: array
                  description: Список номенклатур
                groups:
                  type: array
                  description: Список групп
                units:
                  type: array
                  description: Список единиц измерения
      500:
        description: Ошибка при формировании отчета
    """
    try:
        manager = settings_manager()
        manager.current_settings.report_mode = format_type
        start = start_service( manager.current_settings )

        with open('docs/receipt1.json', 'r', encoding='utf-8') as file:
            start.create(json.load(file))

        factory = report_factory(manager.current_settings)
  
        report = factory.create(None, start.get_storage().get_data())

        result = '{'
        j = 0
        for type in ["recipes","nomenclatures","groups","units"] :
            out = ''    
            data = report.create(type)
            i=0
            result += f'"{type}":'
            if(format_type == "json"): 
                out+="["
                for elem in data:
                    parsed_data = json.loads(elem)
                    corrected_data = common.prepare_json_out(parsed_data)   
                    out+= json.dumps(corrected_data, ensure_ascii=False, indent=4)
                    if (i != len(data)-1):
                        i+=1
                        out+=","
                out+="]"
            else:
                out += f'"{data}"'

            if(j!=3):
                out+=","           
            result += out
            j+=1
        result += '}'
        return result

    except Exception as ex:
            return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug = True)