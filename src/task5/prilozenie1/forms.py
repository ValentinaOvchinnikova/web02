from django import forms
from .models import Patients# Инструмент для создания форм ввода в данном случае
# Класс для ввода пациента данных в форму Исследований
class PatientDataForm(forms.Form):
    patient_id = forms.IntegerField(
        # Подпись к полю которая будет отображаться перед полем ввода
        label='ID of patient',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}), # Как будет отображаться поле(отступы, стиль)
        error_messages={
            'min_value' : 'ID должен быть положительным числом', #Сообщение если ввод цифры меньше 0
            'required': 'Пожалуйста, введите ID' #Сообщение если поле будет пустым
        }
    )
    trial = forms.ChoiceField(
        label="Select the trial", #Подпись к полю
        choices=[],  # Будет заполнено в view
        widget=forms.Select(attrs={'class': 'form-control'}), #Выпадающий список
        initial='', #Изначально поле будет пустым, как значение по умолчанию
        required=True, #Обязательное поле для заполнения
        error_messages={'required':'Выберите исследование из списка. Поле не может быть пустым'})

    condition_score = forms.IntegerField(
        label='Condition score (0-100)',
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control'}), # Поле ввода числа
        error_messages={
            'min_value': 'Score должен быть больше или равен 0',
            'max_value': 'Score должен быть меньше или равен 100',
            'required': 'Пожалуйста, заполните поле'
        }
    )
    drug = forms.ChoiceField(
        label='Select the drug',
        choices=[], #Будет в представлениях
        widget=forms.Select(attrs={'class': 'form-control'}), #Выпадающий список
        initial='', #Изначально поле будет пустым, как значение по умолчанию
        required=True, #Обязательное поле для заполнения
        error_messages={'required': 'Выберите препарат из списка. Поле не может быть пустым'}
        )


# Класс для ввода данных пациента для регистрации
class PatientRegister(forms.Form):
    name = forms.CharField(
        label='Name of patient',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}) #Поле для ввода текста
    )
    age = forms.IntegerField(
        label='Age of patient',
        min_value=0,
        max_value=120,
        widget=forms.NumberInput(attrs={'class': 'form-control'}) #Поле ввода числа
    )
    gender = forms.ChoiceField(
        label='Gender of patient',
        choices=[('Male','Male'), ('Female', 'Female')], #Варианты выбора
        widget=forms.Select(attrs={'class': 'form-control'}) #Выпадающий список
    )
    conditions = forms.CharField(
        label='Diagnos',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}) # Поле для ввода многострочного текста, высотой в 2 строки
    )
