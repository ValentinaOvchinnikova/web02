from django.shortcuts import render
from .models import Trials
from .forms import PatientDataForm


# Create your views here.
def input_form(request):
    # Получаю все исследования из базы данных
    trials = [
        Trials(name='Trial 1', drug='Placebo'),
        Trials(name='Trial 2', drug='Placebo'),
        Trials(name='Trial 3', drug='Placebo'),
        Trials(name='Trial 4', drug='Placebo'),
        Trials(name='Trial 5', drug='Placebo'),
        Trials(name='Trial 6', drug='Placebo'),
        Trials(name='Trial 7', drug='Placebo'),
        Trials(name='Trial 1', drug='Ibuprofen'),
        Trials(name='Trial 2', drug='Ibuprofen'),
        Trials(name='Trial 3', drug='Ibuprofen'),
        Trials(name='Trial 4', drug='Ibuprofen'),
        Trials(name='Trial 5', drug='Ibuprofen'),
        Trials(name='Trial 6', drug='Ibuprofen'),
        Trials(name='Trial 7', drug='Ibuprofen'),
    ]
    if request.method == 'POST':
        form = PatientDataForm(request.POST)

        trial_id = request.POST.get('trial_id')
        select_trial = next((t for t in trials if str(t.id) == trial_id), None)

        if select_trial:
            form.fields['drug'].choices = [('Placebo', 'Ibuprofen'), (select_trial.drug, select_trial.drug)]

        if form.is_valid():
            return render(
                request, 'prilozenie1/success.html', {
                'patient_id' : form.cleaned_data['patient_id'],
                'trial': select_trial,
                'condition': form.cleaned_data['condition_score'],
                'drug': form.cleaned_data['drug']
                })
    else:
        form = PatientDataForm()

    return render(request, 'prilozenie1/input_form.html', {
                    'trials': trials,
                    'form': form
    })