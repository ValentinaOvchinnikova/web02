from django.db import models

# Я определила класс Trials который определяет какие поля будут в моей таблице
# Присвоила тип данных Varchar(100) и verbose_name, поскольку в этом задании бд не используется, взяла рандомные поля

class Trials(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name of trial")
    drug = models.CharField(max_length=100, verbose_name="Name of drug")

    # Исследование будет отображаться как н-р Исследование1 (Плацебо)

    def __str__(self):
        return f"{self.name} ({self.drug})"

#  По итогам django создаст таблицу с полями id, name, drug