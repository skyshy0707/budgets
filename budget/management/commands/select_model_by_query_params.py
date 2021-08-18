# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 15:49:46 2021

@author: SKY_SHY
"""

import json
from django.core.management.base import BaseCommand


from for_serializer.update_data_serializer import get_model

class Command(BaseCommand):
    
    help = "выбирает объект из таблицы <model> по указанным полям"\
        "и их значениям query_params = {'field': 'value'}"
    
    def add_arguments(self, parser):
        
        parser.add_argument("model", help="ссылка на таблицу app.Model")
        parser.add_argument("query_params", help="поле --- параметр запроса к app.Model")
        
    
    def handle(self, model, query_params, *args, **kwargs):
        
        model = get_model(*model.split("."))
        query_params = query_params.replace("\'", "\"")
        query_params = json.loads(query_params)
        
        repr = str([str(obj) 
                    for obj in model.objects.filter(**query_params)])

        return repr