from django.shortcuts import render
from .forms import PatientDataForm


# Функция принимает https запрос
def input_form(request):
    # Это списки для choices=[] в файле forms.py чтобы был выпадающий список
    # В кортеже - первый элемент - значение для формы, второй - отображаемый текст
    trials = [('', '--Select--'),
        ('Trial 1', 'Trial 1'),
        ('Trial 2', 'Trial 2'),
         ('Trial 3', 'Trial 3'),
         ('Trial 4', 'Trial 4'),
         ('Trial 5', 'Trial 5'),
         ('Trial 6','Trial 6'),
         ('Trial 7','Trial 7')
    ]
    drugs = [('', '--Select--'),('Placebo', 'Placebo'),('Ibuprofen', 'Ibuprofen')]

    # Метод пост используется для отправки данных формы на сервер
    if request.method == 'POST':
        form = PatientDataForm(request.POST)
        # После обращения к форме я беру отдельные поля из этой формы и определяю переменные для них
        form.fields['trial'].choices = trials
        form.fields['drug'].choices = drugs

        # Если форма проходит валидацию
        if form.is_valid():
            # Я преобразую списки в словари и получаю очищенные данные формы для читаемых значений выбранных вариантов
            selected_trial = dict(trials).get(form.cleaned_data['trial'])
            selected_drug = dict(drugs).get(form.cleaned_data['drug'])

            # Если форма валидна, то мы переходим на страницу успеха и код заканчивается здесь
            return render(
                request, 'prilozenie1/success.html',
        {
                'patient_id' : form.cleaned_data['patient_id'],
                'trial': selected_trial,
                'condition': form.cleaned_data['condition_score'],
                'drug': selected_drug
                })

    # Если форма не валидна то остаемся на форме ввода данных
    else:
        form = PatientDataForm()
        form.fields['trial'].choices = trials
        form.fields['drug'].choices = drugs

    return render(request, 'prilozenie1/input_form.html', {'form': form})