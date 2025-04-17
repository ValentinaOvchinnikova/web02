from django.db import models
# Модель которая определяет таблицу Trials, ее можно мигрировать в бд
class Trials(models.Model):
    trial_id = models.AutoField(primary_key=True)
    trial_name = models.CharField(max_length=100)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    med = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'trials'  # имя таблицы в бд