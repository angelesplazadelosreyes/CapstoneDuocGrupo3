from django import forms
from .models import PatientData

# Define BOOLEAN_CHOICES como una constante global
BOOLEAN_CHOICES = [(1, 'Sí'), (0, 'No')]

class PatientDataForm(forms.ModelForm):
    class Meta:
        model = PatientData
        fields = [
            'GENDER', 'AGE', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY',
            'PEER_PRESSURE', 'CHRONIC_DISEASE', 'FATIGUE', 'ALLERGY',
            'WHEEZING', 'ALCOHOL_CONSUMING', 'COUGHING', 'SHORTNESS_OF_BREATH',
            'SWALLOWING_DIFFICULTY', 'CHEST_PAIN',
        ]
        labels = {
            'GENDER': 'Sexo',
            'AGE': 'Edad',
            'SMOKING': '¿Fuma?',
            'YELLOW_FINGERS': '¿Tiene los dedos amarillos?',
            'ANXIETY': '¿Sufre de ansiedad?',
            'PEER_PRESSURE': '¿Sufre de presión de grupo?',
            'CHRONIC_DISEASE': '¿Tiene alguna enfermedad crónica?',
            'FATIGUE': '¿Se siente fatigado?',
            'ALLERGY': '¿Tiene alergias?',
            'WHEEZING': '¿Tiene sibilancias?',
            'ALCOHOL_CONSUMING': '¿Consume alcohol?',
            'COUGHING': '¿Tiene tos?',
            'SHORTNESS_OF_BREATH': '¿Siente falta de aire?',
            'SWALLOWING_DIFFICULTY': '¿Tiene dificultad para tragar?',
            'CHEST_PAIN': '¿Tiene dolor en el pecho?',
        }
        widgets = {
            'GENDER': forms.RadioSelect(
                choices=PatientData.GENDER_CHOICES,  
                attrs={'class': 'form-check-input'}
            ),
            'AGE': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 100px;',
                'placeholder': 'Ej.: 21',
                'min': '21',
                'max': '87',
                'required': 'true',
            }),
            # Uso de BOOLEAN_CHOICES global
            **{
                field: forms.RadioSelect(
                    choices=BOOLEAN_CHOICES,
                    attrs={'class': 'form-check-input'}
                )
                for field in [
                    'SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE',
                    'CHRONIC_DISEASE', 'FATIGUE', 'ALLERGY', 'WHEEZING',
                    'ALCOHOL_CONSUMING', 'COUGHING', 'SHORTNESS_OF_BREATH',
                    'SWALLOWING_DIFFICULTY', 'CHEST_PAIN',
                ]
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['GENDER'].initial = 1  # Valor predeterminado: Masculino