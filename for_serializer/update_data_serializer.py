import json
import numpy as np

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

def get_model(app_label, model):
    """
    возвращает таблицу модели данных
    по переданным параметрам ---
    названию приложения app_label и 
    названию модели model
    """
    return apps.get_model(app_label, model)

def get_obj_by_field_value(refilling_fields, data, name_field):
    """
    возвращает экз. указанной модели app.Model.field, которая
    назначена для поля name_field в словаре refilling_fields
    по ключу 'map'
    """
    
    # получаем таблицу объектов Model:
    model_params = refilling_fields[name_field]["map"].split(".")[:2]
    model_obj = get_model(*model_params)
        
    # извлекаем поле, по которому будем искать объект модели:
    field = refilling_fields[name_field]["map"].split(".")[-1]
    kwargs = {field: data[name_field]}
    
    #
    return model_obj.objects.get(**kwargs)

def rename_dields(renaming_fields, data):
    """
    обновляет названия полей в переданном аргументе 
    data, заменяя их на новые значения, которые соотвествуют
    старым названиям, найденным по ключам в renaming_fields
    
    Метод возвращает обновлённую структуру data в соотвествии 
    с изменениями, указанными в renaming_fields
    """
    
    for name_field in renaming_fields.keys():
        
        rewr_value = data.pop(name_field)
        data.update({renaming_fields[name_field]: rewr_value})
        
    return data
   
def rerecord_values(refilling_fields, data):
    """
    обновляет значения полей в переданном аргументе 
    data, заменяя их на новые значения, в порядке, определямом 
    по значениям ключей в словаре refilling_fields, 
    соотвествующие названиям полей в data.
    
    Названиям полей в refilling_fields соотвествует словарь,
    например:
    
    "parentcode": {"map": "budget.Budget.code", "fill": "id"}
    
    По ключу 'map' определяется имя таблицы модели данных, в 
    данном случае это Budget и критерий выбора экз. модели --- 
    в данном случае это поле 'code', которому соотвесвует 
    значение поля 'parentcode' в data. Выбор экз. модели 
    использует синтаксис Model.objects.get в методе 
    get_obj_by_field_value, поэтому необходимо убедиться, что
    поле 'code' уникально.
    
    а по ключу 'fill' определяется имя поля в выбранной таблице, 
    данными которого следует заполнить поле 'parentcode'.
    
    
    Метод возвращает обновлённую структуру data в соотвествии 
    с изменениями, указанными в refilling_fields
    """
    
    
    for name_field in refilling_fields.keys():
        
    
        assert set(refilling_fields[name_field].keys()) == {"map", "fill"}, \
            "Переданы некорректные значения ключей соотвествия"
        
        try:
            model = get_obj_by_field_value(refilling_fields, data, name_field)
        except ObjectDoesNotExist:
            rewr_value = ""
        else:
            rewr_value = getattr(model, refilling_fields[name_field]["fill"])
        data.update({name_field: rewr_value})
        
    return data
    
def data_upd(renaming_fields, refilling_fields, data):
    """
    Метод возвращает обновлённую структуру data в соотвествии 
    с изменениями, указанными в renaming_fields, refilling_fields
    """
    
    data = rename_dields(renaming_fields, data)
    data = rerecord_values(refilling_fields, data)
    
    return data

def get_list(string, delimeter=","):
    """
    парсит строку, превращая её в список
    """
    
    list_params = string.split(delimeter)
    
    return list(np.char.strip(list_params))

def get_kwargs_for_universal_serializer(request):
    """
    извлекает параметры из запроса клиента, необходимые 
    для инициализации сериализатора
    """
    
    params = {}
    query = request.query_params
    
    for param in query.keys():
        
        if param == "model":
            item = {param: query["model"]}
        elif param in {"serialize_fields",}:
            item = {param: get_list(query[param])}
        elif param in {"renaming_fields", 
                       "refilling_fields"}:
            item = {param: json.loads(query[param])}
            
        params.update(item)


    return params 

def get_actual_fields_names_in_apidata(renaming_fields, select_by_fields):
    #получаем имена полей, находящиеся в элементе данных,
    #полученных от внешнего api:
            
    actual_data_fields = []   
    
    original_fields = dict(zip(renaming_fields.values(), renaming_fields.keys()))
    
    for field in select_by_fields:
        
        actual_data_field = field
        if field in original_fields:
            actual_data_field = original_fields[field]
        
        actual_data_fields.append(actual_data_field)
        
    return actual_data_fields   