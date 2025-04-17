from django import forms # Инструмент для создания форм ввода в данном случае
# Класс, который будет описывать форму ввода данных, характеристики полей
class PatientDataForm(forms.Form):
    patient_id = forms.IntegerField(
        # Подпись к полю которая будет отображаться перед полем ввода
        label='ID of patient',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        error_messages={
            'min_value' : 'ID должен быть положительным числом',
            'required': 'Пожалуйста, введите ID'
        }
    )
    trial = forms.ChoiceField(
        label="Select the trial",
        choices=[],  # Будет заполнено в view
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='',
        required=True,
        error_messages={'required':'Выберите исследование из списка. Поле не может быть пустым'})

    condition_score = forms.IntegerField(
        label='Condition score (0-100)',
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        error_messages={
            'min_value': 'Score должен быть больше или равен 0',
            'max_value': 'Score должен быть меньше или равен 100',
            'required': 'Пожалуйста, заполните поле'
        }
    )
    drug = forms.ChoiceField(
        label='Select the drug',
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='',
        required=True,
        error_messages={'required': 'Выберите препарат из списка. Поле не может быть пустым'}
        )

