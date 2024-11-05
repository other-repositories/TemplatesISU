
import json 


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
        