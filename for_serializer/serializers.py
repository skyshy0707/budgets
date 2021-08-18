from for_serializer.update_data_serializer import get_model, data_upd
from rest_framework import serializers

from rest_framework.fields import empty


"""
модуль с классом универсального сериализатора UnSerializer
"""
    
class UnSerializer(serializers.ModelSerializer):
    
    """
    конструктор класса принимает след. аргументы:
    
    instance --- экз. объекта модели данных, для его редактирования
    
    data --- данные, используемые для обновления экз. объекта модели данных
             (put-запрос)
             
    model --- сслыка на модель в синтаксисе django 
             '<имя_приложения>.<Класс_модели>', тип str
             
    editable_fields --- перечень сериализуемых полей модели, список строк
    
    renaming_fields --- словарь, содержащий ключи имён полей в data, которые 
                        необходимо заменить на значения, найденные по 
                        таким ключам в renaming_fields
                        
    refilling_fields --- словарь, определяющий особый порядок заполнения
                       полей модели model, отличный от значения, указанного в 
                       data. Ключами данного словаря являются имена полей
                       модели model, а значения определяют порядок их 
                       заполнения.
                       
                       Значение имеет структуру словаря след. вида:
                           {'map': '<имя_приложения>.<Класс_модели>.<поле1>', 
                            'fill': <поле2>}
                           
                       Ключ 'map' определяет django-модель класса 
                       <Класс_модели>, которое находится в приложении 
                       <имя_приложения> и поле <поле1>, по которому следует 
                       выбрать этот экземпляр. Значение поля <поле1> находится
                       в data, найденное по ключу в refilling_fields
                       
                       Ключ 'fill' указывает на поле в выбранном экз. 
                       <имя_приложения>.<Класс_модели>, согласно 'map'. 
                       Значением этого поля и следует заполнить редактируемый
                       или создаваемый экземпляр модели model, 
                       вместо указанного значения в data
    """

    def __init__(self, instance=None, data=empty, model=None, 
                 serialize_fields=None, renaming_fields={}, refilling_fields={}, 
                 **kwargs):
        
        serializers.ModelSerializer.__init__(self, instance=instance, data=data,
                                             **kwargs)
        
        
        self.Meta.model = get_model(*model.split("."))
        self.Meta.fields = serialize_fields
        self.renaming_fields = renaming_fields
        self.refilling_fields = refilling_fields
        
    
    class Meta:
        pass
    
    
    def to_internal_value(self, data):
        
        for field in data.keys():
            if data.get(field) == "":
                data[field] = None

        data = data_upd(self.renaming_fields, self.refilling_fields, data)
    
        return super(UnSerializer, self).to_internal_value(data)