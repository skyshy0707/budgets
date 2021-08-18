import datetime
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.



class KBKStatus(models.TextChoices):
    
    ACTIVE = "ACTIVE", _('Актуальная запись')
    ARCHIVE = "ARCHIVE", _('Архивная запись')


class BudgetType(models.TextChoices):
    """Код типа бюджета"""
    OTHER = "00", _('Прочие бюджеты')
    FEDERAL = "01", _('Федеральный бюджет')
    SUBJECT = "02", _('Бюджет субъекта РФ')
    CAPITALS = "03", _('Бюджеты внутригородских МО г. Москвы и г. Санкт-Петербурга')
    CITY = "04", _('Бюджет городского округа')
    MUNICIPAL = "05", _('Бюджет муниципального района')
    PENSION = "06", _('Бюджет Пенсионного фонда РФ')
    FSS = "07", _('Бюджет ФСС РФ')
    FFOMS = "08", _('Бюджет ФФОМС')
    TFOMS = "09", _('Бюджет ТФОМС')
    LOCAL = "10", _('Бюджет поселения')
    CITY_DIST = "11", _('Бюджет городского округа с внутригородским делением')
    CITY_AREA = "12", _('Бюджет внутригородского района')
    URBAN_SETTLEMENT = "13", _('Бюджет городского поселения')
    MUN_DIST = "14", _('Бюджет муниципального округа')
    #Есть 13 код в документации не описан, возможно есть и другие
    # ДОБАВИЛ КОДЫ 11, 12, 13 --- см. строки выше
    DISTRIBUTED = "98", _('Распределяемый доход')
    ORGANIZATION = "99",_('Доход организации (только для ПДИ)')
    
    __empty__ = _('(Unknown)')




class Budget(models.Model):
   # guid                = models.CharField("Глобально-уникальный идентификатор записи", max_length=36)  # ! Не берем при импорте
   code = models.CharField("Код", max_length=8, blank=False, null=False)
   name = models.TextField("Полное наименование", max_length=2000, blank=False, null=False)
   parentcode = models.ForeignKey('self', verbose_name="Вышестоящий бюджет", blank=True, null=True, on_delete=models.SET_NULL)
   startdate = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now)
   enddate = models.DateTimeField("Дата окончания действия записи", blank=True, null=True, default=None)
   status = models.CharField("Статус записи", max_length=7, choices=KBKStatus.choices, blank=False, null=False, default=KBKStatus.ACTIVE)
   budgettype = models.CharField("Тип бюджета", max_length=2, choices=BudgetType.choices, blank=False, null=False, default=BudgetType.OTHER)

   class Meta:
       verbose_name = 'Справочник бюджетов'
       verbose_name_plural = 'Справочники бюджетов'

   def __str__(self):
       return f"{self.code}: {self.name}"

class GlavBudgetClass(models.Model):
   """Справочник главы по бюджетной классификации."""

   # guid                = models.CharField("Глобально-уникальный идентификатор записи", max_length=36)
   code = models.CharField("Код", max_length=3, blank=False, null=False)  # ! если не будут пересекаться добавить: , unique=True
   name = models.TextField("Сокращенное наименование", max_length=254, blank=True, null=True)
   startdate = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now)
   enddate = models.DateTimeField("Дата окончания действия записи", null=True)
   budget = models.OneToOneField(Budget, verbose_name="Бюджет", blank=False, null=False, on_delete=models.CASCADE)
   # tofkcode
   # ppocode
   #dateinclusion       = models.DateTimeField("Дата включения кода", blank=False, null=False, default=datetime.datetime.now)
   #dateexclusion       = models.DateTimeField("Дата исключения кода")
   # year                = models.DateField("Год")

   class Meta:
       verbose_name = 'Справочник главы по бюджетной классификации'
       verbose_name_plural = 'Справочники главы по бюджетной классификации'

   def __str__(self):
       return f"{self.code}: {self.name}"
   
    
admin.site.register(Budget)

