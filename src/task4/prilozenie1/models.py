from django.db import models
# Модель которая определяет таблицу Trials, Measurements, Patients ее можно мигрировать в бд
class Patients(models.Model):
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    conditions = models.CharField(max_length=100)

    class Meta:
        # Таблица которая есть в бд
        db_table = 'patients'


class Trials(models.Model):
    trial_id = models.AutoField(primary_key=True)
    trial_name = models.CharField(max_length=100)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    med = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        # Таблица которая есть в бд
        db_table = 'trials'


class Measurements(models.Model):
    measurement_id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patients, on_delete=models.DO_NOTHING, db_column='patient_id')
    trial_id = models.ForeignKey(Trials, on_delete=models.DO_NOTHING, db_column='trial_id')
    measurement_date = models.DateField(auto_now_add=True)
    drug = models.CharField(max_length=100)
    condition_score = models.IntegerField()

    class Meta:
        # Таблица которая есть в бд
        db_table = 'measurements'
