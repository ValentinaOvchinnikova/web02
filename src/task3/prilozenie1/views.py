from django.shortcuts import render
from .models import Trials
from .forms import PatientDataForm



# Функция возвращает анализ данных о самочувствии в зависимости от введенной цифры

def an_condition(condition_score):
    if condition_score < 30:
        return "Тяжелое состояние"
    elif 30 <= condition_score < 60:
        return "Среднетяжелое состояние"
    elif condition_score >= 60:
        return "Удовлетворительное состояние"

# Функция принимает https запрос
def input_form(request):
    # Получаю все исследования из базы данных
    trial_form_db = Trials.objects.only('trial_name', 'med')
    # Список для выпадающего меню исследований
    trial_choices = [('', '--Select--')] + [(trial.trial_name, trial.trial_name) for trial in trial_form_db]
    # Формирование списка препаратов где всегда есть плацебо
    drug_choices = [('', '--Select--'), ('Placebo', 'Placebo')]
        # Уникальные препараты из исследований, для каждого свой
    # if trial.med пропускает пустые значения
    unique_drugs = {trial.med for trial in trial_form_db if trial.med}

    # сортирую в алфавитном порядке, добавляю препараты в виде кортежа в список кортежей drug_choices
    for med in sorted(unique_drugs):
        drug_choices.append((med, med))
    # После обращения к форме я беру отдельные поля из этой формы и определяю переменные для них
    if request.method == 'POST':
        form = PatientDataForm(request.POST)
        form.fields['trial'].choices = trial_choices
        form.fields['drug'].choices = drug_choices


        if form.is_valid():
            # Получаю очищенное выбранное значение из формы ввода
            selected_trial_name = form.cleaned_data['trial']
            # Обращаюсь к модели trials
            # filter(trial_name=selected_trial_name) фильтрую записи в бд и получаю значение полученное из формы
            selected_trial = Trials.objects.filter(trial_name=selected_trial_name).first()
            selected_drug = form.cleaned_data['drug']
            # Если выбрано не плацебо и не препарат из конкретного исследования вызывается ошибка
            if selected_drug != 'Placebo' and selected_trial and selected_drug != selected_trial.med:
                form.add_error('drug', 'This drug not in this trial')
            else:
                # Если проверки пройдены, то получаю оценку состояния и вспомогательную функцию анализа самочувствия
                condition_score = form.cleaned_data['condition_score']
                analysis_result = an_condition(condition_score)


                # Возвращаю форму успешного ввода
                return render(
                    request, 'prilozenie1/success.html',
            {
                    'patient_id' : form.cleaned_data['patient_id'],
                    'trial': selected_trial_name,
                    'condition': condition_score,
                    'drug': selected_drug,
                    'analysis': analysis_result
                    })
    # Если форма не прошла проверки, то вызывается эта часть кода
    # Если запрос был гет или форма не прошла валидацию, то возвращает форму ввода с ошибками
    else:
        form = PatientDataForm()
        form.fields['trial'].choices = trial_choices
        form.fields['drug'].choices = drug_choices

    return render(request, 'prilozenie1/input_form.html', {'form': form})