from django import forms # Инструмент для создания форм ввода в данном случае

class PatientDataForm(forms.Form):
    patient_id = forms.IntegerField(
        label='ID of patient',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    condition_score = forms.IntegerField(label='Condition score (0-100)', min_value=0, max_value=100,
                                         widget=forms.NumberInput(attrs={'class': 'form-control'}))
    drug = forms.ChoiceField(label='drug', choices=[], widget=forms.Select(attrs={'class': 'form-control'}))