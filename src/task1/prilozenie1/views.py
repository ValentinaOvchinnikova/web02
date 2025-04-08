from django.shortcuts import render
from .models import Trials
from .forms import PatientDataForm


# Create your views here.
def input_form(request):
    # Это списки для choices=[] в файле forms.py чтобы был выпадающий список
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
    if request.method == 'POST':
        form = PatientDataForm(request.POST)
        form.fields['trial'].choices = trials
        form.fields['drug'].choices = drugs
        if form.is_valid():
            selected_trial = dict(trials).get(form.cleaned_data['trial'])
            selected_drug = dict(drugs).get(form.cleaned_data['drug'])
            return render(
                request, 'prilozenie1/success.html',
        {
                'patient_id' : form.cleaned_data['patient_id'],
                'trial': selected_trial,
                'condition': form.cleaned_data['condition_score'],
                'drug': selected_drug
                })

    else:
        form = PatientDataForm()
        form.fields['trial'].choices = trials
        form.fields['drug'].choices = drugs

    return render(request, 'prilozenie1/input_form.html', {'form': form})