
import json 
from src.settings_manager import settings_manager

class common:
    
    """
    Получить список полей любой модели
    is_common = True - исключить из списка словари и списки
    """
    @staticmethod
    def  prepare_json_out(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    try:
                        nested_value = json.loads(value)
                        data[key] = common.prepare_json_out(nested_value)
                    except json.JSONDecodeError:
                        pass
                elif isinstance(value, dict) or isinstance(value, list):
                    data[key] = common.prepare_json_out(value)
        elif isinstance(data, list):
            for i in range(len(data)):
                if isinstance(data[i], str):
                    try:
                        nested_value = json.loads(data[i])
                        data[i] = common.prepare_json_out(nested_value)
                    except json.JSONDecodeError:
                        pass
                elif isinstance(data[i], dict) or isinstance(data[i], list):
                    data[i] = common.prepare_json_out(data[i])
        
        return data
    
    @staticmethod
    def prepare_array_json(data):
        out = ''
        out += "["
        i=0
        for elem in report.create("storage_row_model"):
            corrected_data = common.prepare_json_out(elem)
            out += json.dumps(corrected_data, ensure_ascii=False, indent=4)
            if i != len(data) - 1:
                i += 1
                out += ","
        out += "]"
        return out
    
    @staticmethod
    def process_report_data(type, format_type, manager, factory, start):
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


        