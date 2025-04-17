from django.shortcuts import render
from .models import Trials
from .forms import PatientDataForm


# Функция принимает https запрос
def input_form(request):
    # Это списки для choices=[] в файле forms.py чтобы был выпадающий список, который динамически берет данные из бд
    trials = [('', '--Select--')] + [(t.trial_name, t.trial_name) for t in Trials.objects.all()]

    drugs = [('', '--Select--'),('Placebo', 'Placebo')]
    # Получение уникальных значений препаратов.
    # exclude(med__exact='') исключает пустые поля
    # Из поля med получаю с помощью values_list('med', flat=True) обычный список(не список кортежей)
    # distinct() убирает дубликаты
    meds = Trials.objects.exclude(med__exact='').values_list('med', flat=True).distinct()
    # Добавляю препарат из бд в новый список drugs в формате (значение, отображение)
    drugs += [(med, med) for med in meds]
    # Метод пост используется для отправки данных формы на сервер
    if request.method == 'POST':
        form = PatientDataForm(request.POST)
        # После обращения к форме я беру отдельные поля из этой формы и определяю переменные для них
        form.fields['trial'].choices = trials
        form.fields['drug'].choices = drugs
        if form.is_valid():
            # Сначала получаю значение поля trial из формы
            # trials - список кортежей
            # name - вернет отображаемое имя при совпадении
            # Если совпадения нет то вернет пустую строку
            selected_trial = next((name for value, name in trials if value == form.cleaned_data['trial']), '')
            selected_drug = next((name for value, name in drugs if value == form.cleaned_data['drug']), '')

            # Рендеринг страницы успеха если форма прошла валидацию
            return render(
                request, 'prilozenie1/success.html',
        {
                'patient_id' : form.cleaned_data['patient_id'],
                'trial': selected_trial,
                'condition': form.cleaned_data['condition_score'],
                'drug': selected_drug
                })
    # Если запрос был гет или форма не прошла валидацию, то возвращает форму ввода с ошибками
    else:
        form = PatientDataForm()
        form.fields['trial'].choices = trials
        form.fields['drug'].choices = drugs

    return render(request, 'prilozenie1/input_form.html', {'form': form})