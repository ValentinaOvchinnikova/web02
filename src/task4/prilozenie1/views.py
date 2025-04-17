from django.shortcuts import render, redirect
from .models import Trials, Patients, Measurements
from .forms import PatientDataForm, PatientRegister

# Возвращает строку оценки самочувствия пациента
def an_condition(condition_score):
    if condition_score < 30:
        return "Тяжелое состояние"
    elif 30 <= condition_score < 60:
        return "Среднетяжелое состояние"
    elif condition_score >= 60:
        return "Удовлетворительное состояние"

# Функция принимает https запрос
def input_form(request):
    # Получаю все исследования из базы данных (столбцы trial_name, med)
    trial_form_db = Trials.objects.only('trial_name', 'med')
    # Список для выпадающего меню исследований
    trial_choices = [('', '--Select--')] + [(t.trial_name, t.trial_name) for t in trial_form_db]

    # Инициализация переменных
    drug_choices = [('', '--Select--'), ('Placebo', 'Placebo')]
    # Переменная для хранения выбранного исследования
    selected_trial = ''
    # Словарь для начальных данных формы
    initial_data = {}

    # Обработка GET-запроса (включая возврат из регистрации)
    # При первом гет запросе показывается пустая форма
    # Если пациент не найден то идет сохранение сессии и перенаправка на форму регистрации
    # 1) Проверяю наличие сохраненных данных в сессии
    if request.method == 'GET':
        measurement_data = request.session.get('measurement_data', {})
        # Восстанавливаем данные из сессии если пациент существует
        if measurement_data and measurement_data.get('patient_exists', False):
            # Для автозаполнения формы
            initial_data = {
                'patient_id': measurement_data['patient_id'],
                'trial': measurement_data['trial'],
                'drug': measurement_data['drug'],
                'condition_score': measurement_data['condition_score']
            }
            # Обновляю список препаратов для выбранного исследования
            selected_trial = initial_data['trial']

            # Обновляем список препаратов для сохраненного исследования
            if selected_trial:
                trial = Trials.objects.filter(trial_name=selected_trial).first()
                if trial and trial.med:
                    drug_choices = [('', '--Select--'), ('Placebo', 'Placebo'), (trial.med, trial.med)]

            # Очищаем сессию после использования
            del request.session['measurement_data']
            request.session.modified = True

    # Обработка POST-запроса (отправка основной формы)
    elif request.method == 'POST':
        form = PatientDataForm(request.POST)
        selected_trial = request.POST.get('trial', '')

        # Обновляем список препаратов для выбранного исследования
        if selected_trial:
            trial = Trials.objects.filter(trial_name=selected_trial).first()
            if trial and trial.med:
                drug_choices = [('', '--Select--'), ('Placebo', 'Placebo'), (trial.med, trial.med)]

        form.fields['trial'].choices = trial_choices
        form.fields['drug'].choices = drug_choices

        if form.is_valid():
            # Обработка валидных данных
            patient_id = form.cleaned_data['patient_id']
            trial_name = form.cleaned_data['trial']
            drug = form.cleaned_data['drug']
            condition_score = form.cleaned_data['condition_score']
            # Ищет пациента и исследование в бд
            try:
                # Поиск пациента
                patient = Patients.objects.get(patient_id=patient_id)
                trial = Trials.objects.get(trial_name=trial_name)

                # Проверка соответствия препарата исследованию
                if drug not in ['Placebo', trial.med]:
                    form.add_error('drug', 'Этот препарат не участвует в исследовании')
                    return render(request, 'prilozenie1/input_form.html', {
                        'form': form,
                        'trial_choices': trial_choices,
                        'drug_choices': drug_choices,
                        'selected_trial': selected_trial
                    })

                # Создание записи измерения
                Measurements.objects.create(
                    patient_id=patient,
                    trial_id=trial,
                    drug=drug,
                    condition_score=condition_score
                )
                # Возвращение страницы успеха
                return render(request, 'prilozenie1/success.html', {
                    'patient': patient,
                    'trial': trial_name,
                    'score': condition_score,
                    'drug': drug,
                    'analysis': an_condition(condition_score)
                })

            #  Если пациент не найден сохраняю данные в сессии и происходит редикт на страницу регистрации
            except Patients.DoesNotExist:
                # Сохранение данных в сессии для регистрации
                request.session['measurement_data'] = {
                    'patient_id': patient_id,
                    'trial': trial_name,
                    'drug': drug,
                    'condition_score': condition_score,
                    'patient_exists': False
                }
                request.session.modified = True
                return redirect('add_patient')

        else:
            # Обработка невалидной формы
            selected_trial = request.POST.get('trial', '')

    # Создание формы с актуальными данными
    form = PatientDataForm(initial=initial_data) if request.method == 'GET' else PatientDataForm(request.POST)
    form.fields['trial'].choices = trial_choices
    form.fields['drug'].choices = drug_choices

    return render(request, 'prilozenie1/input_form.html', {
        'form': form,
        'trial_choices': trial_choices,
        'drug_choices': drug_choices,
        'selected_trial': selected_trial
    })


def add_patient(request):
    # Получаю сохраненные данные из сессии
    measurement_data = request.session.get('measurement_data', {})

    # Проверка условий для доступа к форме регистрации
    if not measurement_data or measurement_data.get('patient_exists', False):
        return redirect('input_form')
    # Создание нового пациента
    if request.method == 'POST':
        form = PatientRegister(request.POST)
        if form.is_valid():
            # Создание нового пациента
            Patients.objects.create(
                patient_id=measurement_data['patient_id'],
                name=form.cleaned_data['name'],
                age=form.cleaned_data['age'],
                gender=form.cleaned_data['gender'],
                conditions=form.cleaned_data['conditions']
            )
            # Обновление сессии и возврат к основной форме
            measurement_data['patient_exists'] = True
            request.session['measurement_data'] = measurement_data
            request.session.modified = True
            return redirect('input_form')
    else:
        form = PatientRegister()

    return render(request, 'prilozenie1/add_patient.html', {'form': form})


def success(request):
    return render(request, 'prilozenie1/success.html')