import os
import io
from urllib import request
import joblib
import numpy as np
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import redirect, render
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.shortcuts import redirect

from .forms import PatientDataForm
from .models import PredictionHistory
from .predict_model import predict_tumor_category


### Funciones Auxiliares ###

def generate_pdf_data(patient_data, prediction_result, prediction_proba):
    """
    Genera un diccionario con los datos ingresados por el usuario y los resultados de la predicción.
    """
    factors = [
        ("Fuma", patient_data.SMOKING),
        ("Dedos amarillos", patient_data.YELLOW_FINGERS),
        ("Ansiedad", patient_data.ANXIETY),
        ("Presión de pares", patient_data.PEER_PRESSURE),
        ("Enfermedad crónica", patient_data.CHRONIC_DISEASE),
        ("Fatiga", patient_data.FATIGUE),
        ("Alergia", patient_data.ALLERGY),
        ("Silbido en el pecho", patient_data.WHEEZING),
        ("Consumo de alcohol", patient_data.ALCOHOL_CONSUMING),
        ("Tos", patient_data.COUGHING),
        ("Dificultad para respirar", patient_data.SHORTNESS_OF_BREATH),
        ("Dificultad para tragar", patient_data.SWALLOWING_DIFFICULTY),
        ("Dolor en el pecho", patient_data.CHEST_PAIN),
    ]
    positive_factors = [name for name, value in factors if value == 1]
    


    return {
        "AGE": patient_data.AGE,
        "GENDER": "Masculino" if patient_data.GENDER == 1 else "Femenino",
        "positive_factors": positive_factors,
        "prediction_result": (
            "Usted tiene una alta probabilidad de presentar cáncer de pulmón. "
            "Le recomendamos que consulte a un médico." if prediction_result == 1 else
            "Es poco probable que usted tenga cáncer de pulmón. Sin embargo, le recomendamos "
            "que consulte a un médico si tiene alguna preocupación."
        ),
        "prediction_proba": prediction_proba * 100,  # Convertir a porcentaje
    }


### Vistas Principales ###

def perform_prediction(request, session_data):
    """
    Realizar la predicción utilizando los datos de la sesión y redirigir a la página de resultados.
    """
    # Validar los datos finales
    form = PatientDataForm(session_data)
    if not form.is_valid():
        return HttpResponse("Datos inválidos para la predicción.", status=400)

    # Cargar el modelo
    model_path = os.path.join(os.path.dirname(__file__), 'modelo_random_forest.pkl')
    try:
        model = joblib.load(model_path)
        print("Modelo cargado correctamente.")
    except FileNotFoundError:
        return HttpResponse("Modelo de predicción no encontrado.", status=500)

    # Preparar los datos para la predicción
    data = np.array([[
        session_data.get('GENDER'), session_data.get('AGE'), session_data.get('SMOKING'), session_data.get('YELLOW_FINGERS'),
        session_data.get('ANXIETY'), session_data.get('PEER_PRESSURE'), session_data.get('CHRONIC_DISEASE'), session_data.get('FATIGUE'),
        session_data.get('ALLERGY'), session_data.get('WHEEZING'), session_data.get('ALCOHOL_CONSUMING'), session_data.get('COUGHING'),
        session_data.get('SHORTNESS_OF_BREATH'), session_data.get('SWALLOWING_DIFFICULTY'), session_data.get('CHEST_PAIN')
    ]])

    # Realizar la predicción
    prediction_result = model.predict(data)[0]
    prediction_proba = model.predict_proba(data)[0][1] * 100

    # Guardar los resultados en la sesión
    request.session['prediction_result'] = prediction_result
    request.session['prediction_proba'] = prediction_proba

    # Redirigir a la página de resultados
    return redirect('core:prediction_result')



def patient_data_form_fast(request):
    """
    Vista para el formulario rápido de datos del paciente.
    """
    form = PatientDataForm()
    model_path = os.path.join(os.path.dirname(__file__), 'modelo_random_forest.pkl')

    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        print("Modelo no encontrado.")
        model = None

    if request.method == 'POST':
        form = PatientDataForm(request.POST)
        if form.is_valid() and model:
            patient_data = form.save()
            print(f"Datos ingresados por el usuario: {form.cleaned_data}")

            data = np.array([[  
                patient_data.GENDER, patient_data.AGE, patient_data.SMOKING, patient_data.YELLOW_FINGERS,
                patient_data.ANXIETY, patient_data.PEER_PRESSURE, patient_data.CHRONIC_DISEASE, patient_data.FATIGUE,
                patient_data.ALLERGY, patient_data.WHEEZING, patient_data.ALCOHOL_CONSUMING, patient_data.COUGHING,
                patient_data.SHORTNESS_OF_BREATH, patient_data.SWALLOWING_DIFFICULTY, patient_data.CHEST_PAIN
            ]])

            prediction_result = model.predict(data)[0]
            prediction_proba = model.predict_proba(data)[0][1]
            if prediction_proba == 1:
                prediction_proba = 0.9997
            elif prediction_proba == 0:
                prediction_proba = 0.0001
            

            pdf_data = generate_pdf_data(patient_data, prediction_result, prediction_proba)
            request.session.update(pdf_data)

            return render(request, 'core/prediction_result.html', {
                'form': form,
                'prediction_result': prediction_result,
                'prediction_proba': prediction_proba * 100,
                'positive_factors': pdf_data["positive_factors"],
                'pdf_data': pdf_data,
            })

    return render(request, 'core/patient_data_form_fast.html', {'form': form})


def predict_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Obtener la imagen cargada
        image = request.FILES['image']

        # Convertir la imagen en un objeto BytesIO
        image_bytes = io.BytesIO(image.read())

        # Realizar predicción
        result = predict_tumor_category(image_bytes)

        # Depurar para confirmar la estructura de probabilities
        print("Result probabilities:", result['probabilities'])

        # Multiplicar y redondear las probabilidades por 100
        probabilities = [round(float(p) * 100, 2) for p in result['probabilities'][0]]
        print("Processed probabilities:", probabilities)

        # Guardar predicción automáticamente en la base de datos
        prediction = PredictionHistory.objects.create(
            image=image,
            predicted_class=result['class'],
            probabilities=result['probabilities'],
        )

        # Renderizar resultados
        return render(request, 'core/predict_results.html', {
            'class': result['class'],
            'probabilities': probabilities,  # Asegúrate de pasar esto al template
            'uploaded_image_url': prediction.image.url,
        })

    return render(request, 'core/predict.html')



def download_prediction_result(request):
    # Recuperar datos de la sesión
    age = request.session.get("AGE", "N/A")
    gender = request.session.get("GENDER", "N/A")
    positive_factors = request.session.get("positive_factors", [])
    prediction_result = request.session.get("prediction_result", "N/A")
    prediction_proba = request.session.get("prediction_proba", 0.0)

    # Crear un objeto HttpResponse con contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resultado_prediccion.pdf"'

    # Crear un PDF con ReportLab
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Título del informe
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Informe de Resultados de la Predicción")

    # Datos ingresados
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 720, f"Edad: {age}")
    pdf.drawString(100, 700, f"Género: {gender}")
    pdf.drawString(100, 680, "Factores de riesgo positivos:")
    y = 660
    for factor in positive_factors:
        pdf.drawString(120, y, f"- {factor}")
        y -= 20

    # Resultado de la predicción con ajuste de texto
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import getSampleStyleSheet

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    prediction_paragraph = Paragraph(f"Resultado de la predicción: {prediction_result}", normal_style)
    probability_paragraph = Paragraph(f"Probabilidad de padecer cáncer de pulmón: {prediction_proba}%", normal_style)

    prediction_paragraph.wrapOn(pdf, 400, 100)
    prediction_paragraph.drawOn(pdf, 100, y - 10)

    probability_paragraph.wrapOn(pdf, 400, 100)
    probability_paragraph.drawOn(pdf, 100, y - 50)

    # Ajustar posición del gráfico
    y_graph = y - 250

    try:
        # Convertir prediction_proba a float y validar
        proba_value = float(prediction_proba)
        if not (0 <= proba_value <= 100):
            raise ValueError(f"El valor de prediction_proba no está en el rango esperado: {proba_value}")

        # Crear el gráfico
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

        fig = Figure(figsize=(4, 4))
        ax = fig.add_subplot(111)
        ax.pie(
            [proba_value, 100 - proba_value],
            labels=["Probabilidad", "Resto"],
            colors=["#007BFF", "#D8D8D8"],
            autopct='%1.1f%%',
        )
        ax.set_title("Probabilidad de Padecer Cáncer")

        # Convertir el gráfico a imagen
        canvas_graph = FigureCanvas(fig)
        img_buffer = io.BytesIO()
        canvas_graph.print_png(img_buffer)
        img_buffer.seek(0)

        # Añadir el gráfico como imagen al PDF
        pdf.drawImage(ImageReader(img_buffer), 100, y_graph, width=200, height=200)

    except ValueError as ve:
        print(f"Error de conversión o rango inválido: {ve}")
        pdf.drawString(100, y_graph, "Gráfico no disponible: Datos inválidos.")
    except Exception as e:
        print(f"Error inesperado al generar el gráfico: {e}")
        pdf.drawString(100, y_graph, "Gráfico no disponible por datos insuficientes.")

    # Finalizar y guardar el PDF
    pdf.showPage()
    pdf.save()

    # Configurar la respuesta
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response



def prediction_history_view(request):
    """
    Vista para mostrar el historial de predicciones.
    """
    predictions = PredictionHistory.objects.all().order_by('-created_at')
    return render(request, 'core/history.html', {'predictions': predictions})


def success_view(request):
    """
    Vista de éxito.
    """
    return render(request, 'core/success.html')


def step1(request):
    """
    Vista para la primera card del formulario guiado.
    """
    if 'patient_data' not in request.session:
        request.session['patient_data'] = {}

    if request.method == 'POST':
        # Guardar datos en la sesión como enteros
        request.session['patient_data']['AGE'] = int(request.POST.get('AGE', 0))  # Convertimos AGE a número
        request.session['patient_data']['GENDER'] = int(request.POST.get('GENDER', 0))  # Convertimos GENDER a número
        request.session['patient_data']['SMOKING'] = int(request.POST.get('SMOKING', 0))  # Convertimos SMOKING a número
        request.session['patient_data']['YELLOW_FINGERS'] = int(request.POST.get('YELLOW_FINGERS', 0))  # Convertimos YELLOW_FINGERS a número

        # Redirigir al siguiente paso
        return redirect('core:step2')

    # Renderizar la plantilla para la card 1
    return render(request, 'core/step1.html', {
        'AGE': request.session['patient_data'].get('AGE', ''),
        'GENDER': request.session['patient_data'].get('GENDER', ''),
        'SMOKING': request.session['patient_data'].get('SMOKING', ''),
        'YELLOW_FINGERS': request.session['patient_data'].get('YELLOW_FINGERS', ''),
    })



def step2(request):
    """
    Vista para el paso 2 del formulario guiado.
    Maneja los campos: PEER_PRESSURE, ALCOHOL_CONSUMING, ANXIETY.
    """
    if 'patient_data' not in request.session:
        request.session['patient_data'] = {}


    if request.method == 'POST':
        # Actualizar la sesión con los datos enviados
        request.session['patient_data']['PEER_PRESSURE'] = int(request.POST.get('PEER_PRESSURE', 0))
        request.session['patient_data']['ALCOHOL_CONSUMING'] = int(request.POST.get('ALCOHOL_CONSUMING', 0))
        request.session['patient_data']['ANXIETY'] = int(request.POST.get('ANXIETY', 0))

        # Redirigir al siguiente paso
        return redirect('core:step3')

    # Renderizar el formulario con los datos actuales de la sesión
    data = request.session.get('patient_data', {})
    return render(request, 'core/step2.html', data)



def step3(request):
    """
    Vista para el paso 3 del formulario guiado.
    """
    if 'patient_data' not in request.session:
        request.session['patient_data'] = {}


    if request.method == 'POST':
        # Guardar datos en la sesión
        request.session['patient_data']['SWALLOWING_DIFFICULTY'] = int(request.POST.get('SWALLOWING_DIFFICULTY', 0))
        request.session['patient_data']['FATIGUE'] = int(request.POST.get('FATIGUE', 0))
        request.session['patient_data']['CHEST_PAIN'] = int(request.POST.get('CHEST_PAIN', 0))
        request.session['patient_data']['ALLERGY'] = int(request.POST.get('ALLERGY', 0))
        request.session.modified = True  # Marcar la sesión como modificada

        # Redirigir al paso 4
        return redirect('core:step4')

    # Renderizar la plantilla del paso 3
    return render(request, 'core/step3.html', {
        'patient_data': request.session.get('patient_data', {})
    })



def step4(request):
    """
    Vista para el paso 4 del formulario guiado.
    """
    if 'patient_data' not in request.session:
        request.session['patient_data'] = {}

    if request.method == 'POST':
        # Guardar datos en la sesión
        request.session['patient_data']['COUGHING'] = int(request.POST.get('COUGHING', 0))
        request.session['patient_data']['CHRONIC_DISEASE'] = int(request.POST.get('CHRONIC_DISEASE', 0))
        request.session['patient_data']['SHORTNESS_OF_BREATH'] = int(request.POST.get('SHORTNESS_OF_BREATH', 0))
        request.session['patient_data']['WHEEZING'] = int(request.POST.get('WHEEZING', 0))
        request.session.modified = True  # Marcar la sesión como modificada

        # Redirigir al resumen
        return redirect('core:summary')

    # Renderizar la plantilla del paso 4
    return render(request, 'core/step4.html', {
        'patient_data': request.session.get('patient_data', {})
    })



def summary(request):
    """
    Vista para mostrar el resumen de los datos ingresados y realizar la predicción.
    """
    model_path = os.path.join(os.path.dirname(__file__), 'modelo_random_forest.pkl')

    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        print("Modelo no encontrado.")
        model = None

    if request.method == 'POST' and model:
        # Recuperar los datos de la sesión
        data = np.array([[
            int(request.session.get('GENDER', 0)),
            int(request.session.get('AGE', 0)),
            int(request.session.get('SMOKING', 0)),
            int(request.session.get('YELLOW_FINGERS', 0)),
            int(request.session.get('ANXIETY', 0)),
            int(request.session.get('PEER_PRESSURE', 0)),
            int(request.session.get('CHRONIC_DISEASE', 0)),
            int(request.session.get('FATIGUE', 0)),
            int(request.session.get('ALLERGY', 0)),
            int(request.session.get('WHEEZING', 0)),
            int(request.session.get('ALCOHOL_CONSUMING', 0)),
            int(request.session.get('COUGHING', 0)),
            int(request.session.get('SHORTNESS_OF_BREATH', 0)),
            int(request.session.get('SWALLOWING_DIFFICULTY', 0)),
            int(request.session.get('CHEST_PAIN', 0)),
        ]])

        prediction_result = model.predict(data)[0]
        prediction_proba = model.predict_proba(data)[0][1]
        if prediction_proba == 1:
            prediction_proba = 0.9997
        elif prediction_proba == 0:
            prediction_proba = 0.0001

        # Generar datos para el PDF si es necesario
        pdf_data = generate_pdf_data(request.session, prediction_result, prediction_proba)
        request.session.update(pdf_data)

        return render(request, 'core/prediction_result.html', {
            'prediction_result': prediction_result,
            'prediction_proba': prediction_proba * 100,
            'positive_factors': pdf_data["positive_factors"],
        })

    # Traducción de las claves y valores para la plantilla
    translations = {
        'AGE': 'Edad',
        'GENDER': 'Género',
        'SMOKING': '¿Fuma?',
        'YELLOW_FINGERS': '¿Dedos amarillos?',
        'PEER_PRESSURE': '¿Presión de grupo?',
        'ALCOHOL_CONSUMING': '¿Consume alcohol?',
        'ANXIETY': '¿Ansiedad?',
        'SWALLOWING_DIFFICULTY': '¿Dificultad para tragar?',
        'FATIGUE': '¿Fatiga?',
        'CHEST_PAIN': '¿Dolor en el pecho?',
        'ALLERGY': '¿Alergia?',
        'COUGHING': '¿Tos?',
        'CHRONIC_DISEASE': '¿Enfermedad crónica?',
        'SHORTNESS_OF_BREATH': '¿Dificultad para respirar?',
        'WHEEZING': '¿Sibilancias?',
    }

    patient_data = {
        translations.get(k, k): ('Sí' if v == 1 else 'No' if v == 0 else v)
        for k, v in request.session.items()
    }

    # Renderizar la plantilla con los datos traducidos
    return render(request, 'core/summary.html', {
        'patient_data': patient_data,
    })



def process_guided_form(request):
    """
    Vista para procesar el formulario guiado y generar la predicción.
    """
    if request.method == 'POST':
        patient_data = request.session.get('patient_data', {})
        
        # Cargar el modelo
        model_path = os.path.join(os.path.dirname(__file__), 'modelo_random_forest.pkl')
        try:
            model = joblib.load(model_path)
        except FileNotFoundError:
            print("Modelo no encontrado.")
            return render(request, 'core/error.html', {'message': 'Modelo no encontrado.'})

        # Convertir los datos en un array para el modelo
        data = np.array([[  
            patient_data.get('GENDER'), patient_data.get('AGE'), patient_data.get('SMOKING'), patient_data.get('YELLOW_FINGERS'),
            patient_data.get('ANXIETY'), patient_data.get('PEER_PRESSURE'), patient_data.get('CHRONIC_DISEASE'), patient_data.get('FATIGUE'),
            patient_data.get('ALLERGY'), patient_data.get('WHEEZING'), patient_data.get('ALCOHOL_CONSUMING'), patient_data.get('COUGHING'),
            patient_data.get('SHORTNESS_OF_BREATH'), patient_data.get('SWALLOWING_DIFFICULTY'), patient_data.get('CHEST_PAIN')
        ]])

        # Hacer la predicción
        prediction_result = model.predict(data)[0]
        prediction_proba = model.predict_proba(data)[0][1]
        if prediction_proba == 1:
            prediction_proba = 0.9997
        elif prediction_proba == 0:
            prediction_proba = 0.0001

        return render(request, 'core/prediction_result.html', {
            'prediction_result': prediction_result,
            'prediction_proba': prediction_proba * 100,
        })

    return redirect('core:summary')

