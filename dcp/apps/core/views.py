from django.shortcuts import render
from .forms import PatientDataForm
import joblib
import numpy as np
import os

def patient_data_form_guided(request):
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
            # Guardar datos en la base de datos
            patient_data = form.save()

            # Preparar datos para la predicción
            data = np.array([[  
                patient_data.GENDER,  # Ya es numérico en la base de datos
                patient_data.AGE,
                patient_data.SMOKING,
                patient_data.YELLOW_FINGERS,
                patient_data.ANXIETY,
                patient_data.PEER_PRESSURE,
                patient_data.CHRONIC_DISEASE,
                patient_data.FATIGUE,
                patient_data.ALLERGY,
                patient_data.WHEEZING,
                patient_data.ALCOHOL_CONSUMING,
                patient_data.COUGHING,
                patient_data.SHORTNESS_OF_BREATH,
                patient_data.SWALLOWING_DIFFICULTY,
                patient_data.CHEST_PAIN
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

    return render(request, 'core/patient_data_form_guided.html', {'form': form})



def patient_data_form_fast(request):
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
            # Guardar datos en la base de datos
            patient_data = form.save()

            # Preparar datos para la predicción
            data = np.array([[  
                patient_data.GENDER,  # Ya es numérico en la base de datos
                patient_data.AGE,
                patient_data.SMOKING,
                patient_data.YELLOW_FINGERS,
                patient_data.ANXIETY,
                patient_data.PEER_PRESSURE,
                patient_data.CHRONIC_DISEASE,
                patient_data.FATIGUE,
                patient_data.ALLERGY,
                patient_data.WHEEZING,
                patient_data.ALCOHOL_CONSUMING,
                patient_data.COUGHING,
                patient_data.SHORTNESS_OF_BREATH,
                patient_data.SWALLOWING_DIFFICULTY,
                patient_data.CHEST_PAIN
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

    return render(request, 'core/patient_data_form_fast.html', {'form': form})



from django.shortcuts import render

def success_view(request):
    return render(request, 'core/success.html')
