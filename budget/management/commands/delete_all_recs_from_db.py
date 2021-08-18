# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 20:14:33 2021

@author: SKY_SHY
"""

from django.core.management.base import BaseCommand


from for_serializer.update_data_serializer import get_model

class Command(BaseCommand):
    
    help = "удаляет все записи из указанной таблицы, переданной"\
        "параметром model --- процедура handle"
    
    
    def add_arguments(self, parser):
        
        parser.add_argument("model", help="ссылка на таблицу app.Model")
    
    
    def handle(self, model, *args, **kwargs):
        
        model = get_model(*model.split("."))
        model.objects.all().delete()
        


    
    
        