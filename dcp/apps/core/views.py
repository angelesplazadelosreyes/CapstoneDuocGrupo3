from django.shortcuts import render
from .forms import PatientDataForm
import joblib
import numpy as np
import os

def patient_data_form(request):
    form = PatientDataForm()
    prediction_result = None
    prediction_proba = None

    # Cargar el modelo desde la ruta
    model_path = os.path.join(os.path.dirname(__file__), 'modelo_random_forest.pkl')
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        model = None
        print("Modelo no encontrado. Asegúrate de que el archivo 'modelo_random_forest.pkl' esté en la carpeta correcta.")

    if request.method == 'POST':
        form = PatientDataForm(request.POST)
        if form.is_valid() and model:
            # Extraer datos del formulario
            data = np.array([[  
                1 if form.cleaned_data['GENDER'] == 'M' else 0,
                form.cleaned_data['AGE'],
                form.cleaned_data['SMOKING'],
                form.cleaned_data['YELLOW_FINGERS'],
                form.cleaned_data['ANXIETY'],
                form.cleaned_data['PEER_PRESSURE'],
                form.cleaned_data['CHRONIC_DISEASE'],
                form.cleaned_data['FATIGUE'],
                form.cleaned_data['ALLERGY'],
                form.cleaned_data['WHEEZING'],
                form.cleaned_data['ALCOHOL_CONSUMING'],
                form.cleaned_data['COUGHING'],
                form.cleaned_data['SHORTNESS_OF_BREATH'],
                form.cleaned_data['SWALLOWING_DIFFICULTY'],
                form.cleaned_data['CHEST_PAIN']
            ]])

            # Realizar la predicción
            prediction_result = model.predict(data)[0]
            prediction_proba = model.predict_proba(data)[0][1]

            # Redirigir a la página de resultados
            return render(request, 'core/prediction_result.html', {
                'form': form,
                'prediction_result': prediction_result,
                'prediction_proba': prediction_proba
            })

    return render(request, 'core/patient_data_form.html', {'form': form})



from django.shortcuts import render

def success_view(request):
    return render(request, 'core/success.html')
