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



def generate_pdf_data(patient_data, prediction_result, prediction_proba):
    """
    Genera un diccionario con los datos ingresados por el usuario y los resultados de la predicción.
    """
    # Factores de riesgo positivos
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

    # Crear el diccionario con todos los datos
    pdf_data = {
        "AGE": patient_data.AGE,
        "GENDER": "Masculino" if patient_data.GENDER == 1 else "Femenino",
        "positive_factors": positive_factors,
        "prediction_result": (
            "Es probable que usted tenga cáncer de pulmón. Le recomendamos que consulte a un médico."
            if prediction_result == 1
            else "Es poco probable que usted tenga cáncer de pulmón. Sin embargo, le recomendamos que consulte a un médico si tiene alguna preocupación."
        ),
        "prediction_proba": f"{prediction_proba * 100:.2f}%",  # Formatear a porcentaje con 2 decimales
    }

    return pdf_data



def patient_data_form_fast(request):
    form = PatientDataForm()
    prediction_result = None
    prediction_proba = None
    pdf_data = {}  # Diccionario para almacenar los datos ingresados y la predicción

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

            # Generar el diccionario de datos para el PDF
            pdf_data = generate_pdf_data(patient_data, prediction_result, prediction_proba)

            # Guardar datos en la sesión
            request.session["AGE"] = pdf_data["AGE"]
            request.session["GENDER"] = pdf_data["GENDER"]
            request.session["positive_factors"] = pdf_data["positive_factors"]
            request.session["prediction_result"] = pdf_data["prediction_result"]
            request.session["prediction_proba"] = pdf_data["prediction_proba"]

            # Redirigir a la página de resultados
            return render(request, 'core/prediction_result.html', {
                'form': form,
                'prediction_result': prediction_result,
                'prediction_proba': prediction_proba * 100,
                'positive_factors': pdf_data["positive_factors"],  # Enviar factores de riesgo positivos al template
                'pdf_data': pdf_data,  # Pasar el diccionario al template
            })
        else:
            print("Formulario inválido o modelo no encontrado.")

    return render(request, 'core/patient_data_form_fast.html', {'form': form})




from django.shortcuts import render

def success_view(request):
    return render(request, 'core/success.html')


import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


#control z
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
    y_graph = y - 150
    try:
        proba_value = float(prediction_proba)
        fig = Figure(figsize=(4, 4))
        ax = fig.add_subplot(111)
        ax.pie(
            [proba_value, 100 - proba_value],
            labels=["Probabilidad", "Resto"],
            colors=["#007BFF", "#D8D8D8"],
            autopct='%1.1f%%',
        )
        ax.set_title("Probabilidad de Padecer Cáncer")
        canvas_graph = FigureCanvas(fig)
        img_buffer = io.BytesIO()
        canvas_graph.print_png(img_buffer)
        img_buffer.seek(0)

        pdf.drawImage(ImageReader(img_buffer), 100, y_graph, width=200, height=200)
    except Exception as e:
        print(f"Error al generar el gráfico: {e}")
        pdf.drawString(100, y_graph, "Gráfico no disponible por datos insuficientes.")

    # Finalizar y guardar
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response
