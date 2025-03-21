from django.core.exceptions import ObjectDoesNotExist

from django.db import models


class OrderField(models.PositiveIntegerField):

    def __init__(self, for_fields=None ,*args, **kwargs):

        self.for_fields = for_fields

        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        #Проверка есть ли в поле модели какое либо значнеие
        if getattr(model_instance,self.attname) is None:
            try:
               #Создаётся QuerySet, содержащий все объекты текущей модели. 
                #self.model ссылается на саму модель, 
                #а objects.all() возвращает все её записи.
                qs = self.model.objects.all()
                #Проверка, находится ли в for_feilds какое либо поле модели
                if self.for_fields:
                    #словарь где ключ имя поля,которое в for_feilds,а значение это экзмпляр модели 
                    # привязанной к объекту в for_fields
                    query = {field:getattr(model_instance,field)\
                             for field in self.for_fields}
                    #фильтрация всех экзкемпляров модели по словарю query
                    qs = qs.filter(**query)
                    #извлечение порядкового номера указанного атрибута
                    last_item = qs.latest(self.attname)
                    #создание нового порядкового номера путём суммирования предыдущего
                    value = last_item.counter +1
                    #в случае не найденный объктов ранее,задаётся значение нуля 
            except ObjectDoesNotExist:
                value = 0
            #навсегда задаём каждому новому объекту выбранного атрибута значение
            setattr(model_instance,self.attname,value)
            return value 

        else:
            return super().pre_save(model_instance,add)