from django.db import models

# Create your models here.
class data(models.Model):
    operation_system = models.CharField("Тип ОС:", max_length=200)
    version = models.CharField("Версия ОС:",max_length=200)
    architecture = models.CharField("Архитектура:",max_length=200)
    log_history =  models.TextField("История логов:",max_length=200)


