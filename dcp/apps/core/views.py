from django.shortcuts import render,redirect
from .models import PatientData
from .forms import PatientDataForm
import joblib
import numpy as np
import os


def patient_data_form_guided(request):
    
    raise Exception("Vista patient_data_form_guided ejecutada")

    # Paso actual, leído desde los parámetros de la URL
    current_step = int(request.GET.get('step', 1))  # Paso actual, por defecto es 1
    total_steps = 7  # Número total de pasos en el formulario

    # Inicializar datos guardados (en backend)
    if not request.session.get('patient_data'):
        request.session['patient_data'] = {}
        print("Inicializando datos de sesión para patient_data")

    session_data = request.session['patient_data']
    print(f"Paso actual: {current_step}, Total pasos: {total_steps}")
    print(f"Datos actuales en la sesión: {session_data}")

    if request.method == 'POST':
        # Crear el formulario con los datos del POST
        form = PatientDataForm(request.POST)

        if form.is_valid():
            # Guardar los datos de este paso en la sesión
            step_data = form.cleaned_data
            session_data.update(step_data)
            request.session['patient_data'] = session_data

            print(f"Datos acumulados en la sesión después del paso {current_step}: {session_data}")

            # Si estamos en el último paso, procesar los datos finales
            if current_step == total_steps:
                # Crear una instancia del modelo con todos los datos acumulados
                final_form = PatientDataForm(session_data)
                if final_form.is_valid():
                    # Guardar en la base de datos
                    final_form.save()
                    # Limpiar los datos de la sesión
                    del request.session['patient_data']
                    print("Datos enviados al modelo y guardados en la base de datos")
                    print(f"Datos finales procesados: {session_data}")
                    return redirect('core:success')  # Redirigir a una página de éxito
                else:
                    print(f"Errores en el formulario final: {final_form.errors}")
                    # Si el formulario final no es válido, mostrar errores
                    return render(request, 'core/patient_data_form_guided.html', {
                        'form': final_form,
                        'current_step': current_step,
                        'total_steps': total_steps,
                    })

            # Redirigir al siguiente paso
            next_step = current_step + 1
            print(f"Redirigiendo al siguiente paso: {next_step}")
            return redirect(f"{request.path}?step={next_step}")

        else:
            # Si el formulario tiene errores, renderizar con los errores
            print(f"Errores en el formulario del paso {current_step}: {form.errors}")
            return render(request, 'core/patient_data_form_guided.html', {
                'form': form,
                'current_step': current_step,
                'total_steps': total_steps,
            })

    else:
        # Si es una solicitud GET, inicializar el formulario con datos existentes
        initial_data = session_data if current_step > 1 else None
        form = PatientDataForm(initial=initial_data)
        print(f"Inicializando formulario con datos: {initial_data}")

        # Renderizar el formulario del paso actual
        return render(request, 'core/patient_data_form_guided.html', {
            'form': form,
            'current_step': current_step,
            'total_steps': total_steps,
        })

    # Este punto no debería alcanzarse, pero lo manejamos por si acaso.
    print("La vista no generó una respuesta válida. Devolviendo un formulario vacío.")
    return render(request, 'core/patient_data_form_guided.html', {
        'form': PatientDataForm(),
        'current_step': current_step,
        'total_steps': total_steps,
    })





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
        print("Datos enviados desde el formulario:", request.POST)
        form = PatientDataForm(request.POST)
        if form.is_valid() and model:
            #control z
            print("Formulario válido. Datos limpios:", form.cleaned_data)
            # Guardar datos en la base de datos
            if model:
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
                    'prediction_proba': prediction_proba*100
                })
            else:
                print("Modelo no encontrado. No se puede realizar la predicción.")

    return render(request, 'core/patient_data_form_fast.html', {'form': form})



from django.shortcuts import render

def success_view(request):
    return render(request, 'core/success.html')
