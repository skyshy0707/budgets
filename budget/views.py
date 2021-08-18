import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from for_serializer.serializers import UnSerializer
from for_serializer.update_data_serializer import (get_list, 
                                                   get_model, 
                                                   get_kwargs_for_universal_serializer,
                                                   get_actual_fields_names_in_apidata)
# Create your views here.


class BudgetView(APIView):
    
    serializer_class = UnSerializer
    http_method_names = ('get', 'put', 'post')
    
    def get_object(self, *args, **kwargs):
        #получаем параметры из запроса:
        data = self.request.data
        
        
        query = self.request.query_params
        renaming_fields = json.loads(query["renaming_fields"])   
        select_by_fields = get_list(query["edit_instance_by_fields"])
        
        
        #получаем имена полей, находящиеся в элементе данных,
        #полученных от api:
        actual_data_fields = get_actual_fields_names_in_apidata(renaming_fields, 
                                                                select_by_fields)
        
        #получаем значения полей, по которым будем запрашивать 
        #объект из БД:
            
        by_fields = dict(zip(select_by_fields, [data[field] 
                                                for field in actual_data_fields]))
        
        #получаем и возвращаем объект модели:
        model = get_model(*query["model"].split("."))
        
        return model.objects.filter(**by_fields)[0]
    
    
    def put(self, request, format=None):
        """
        функция для редактирования экз. модели
        """
        data = request.data
        kwargs = get_kwargs_for_universal_serializer(request)
        instance = self.get_object()
        serializer = UnSerializer(instance, data=data, **kwargs)
        
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def post(self, request, format=None):
        """
        функция для создания нового экз. модели
        """
        data = request.data
        kwargs = get_kwargs_for_universal_serializer(request)
        serializer = UnSerializer(data=data, **kwargs)
        
        
        try: 
            self.get_object()
        except IndexError:
            pass
        else:
            return Response(data, status=status.HTTP_409_CONFLICT)
        
            
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        print("errors", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    
    def get(self, request, code, format=None):
        """
        функция для получения экз. модели
        """
        budget = self.get_object()
        
        serializer = UnSerializer(budget)
        return Response(serializer.data, safe=False)
        




"""
класс ObjListView как дополнение --- не входит в задание
"""
class ObjListView(ListAPIView,):

    http_method_names = ('get',)
    
    
    def get_serializer_class(self,):
        
        return UnSerializer
    

    def get_queryset(self,):
        
        """
        возвращает список объектов, выбранных по параметру запроса, 
        указанному по ключу query_param
        """
        query = self.request.query_params
        by_field = json.loads(query["query_param"])
        model = get_model(*query["model"].split("."))
        
        return model.objects.filter(**by_field)
    
    
    def get_serializer(self, *args, **kwargs):
        
        
        kwargs = get_kwargs_for_universal_serializer(self.request)
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        
        return serializer_class(self.paginate_queryset(queryset),
                                many=True,
                                **kwargs)
    
    def list(self, request):
        
        
        serializer = self.get_serializer()
        return self.get_paginated_response(serializer.data)


    
        
        