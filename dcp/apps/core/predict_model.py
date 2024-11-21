import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Ruta al modelo
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'lung_tumor_classifier.h5')

# Cargar el modelo
def load_tumor_model():
    model = load_model(MODEL_PATH)
    return model

# Función para realizar predicciones
def predict_tumor_category(image_path):
    # Cargar el modelo
    model = load_tumor_model()

    # Preprocesar la imagen
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Realizar predicción
    prediction = model.predict(img_array)
    class_idx = np.argmax(prediction)
    class_names = ['benign', 'malignant', 'normal']

    return {
        'class': class_names[class_idx],
        'probabilities': prediction.tolist()
    }
