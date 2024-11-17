from django import forms
from .models import PatientData

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
            'GENDER': forms.RadioSelect(attrs={'class': 'form-check-input',}),
            'AGE': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 100px;',
                'placeholder': 'Ej.: 21',
                'min': '21',
                'max': '87',
                'required': 'true',
            }),
            'SMOKING': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'YELLOW_FINGERS': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'ANXIETY': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'PEER_PRESSURE': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'CHRONIC_DISEASE': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'FATIGUE': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'ALLERGY': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'WHEEZING': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'ALCOHOL_CONSUMING': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'COUGHING': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'SHORTNESS_OF_BREATH': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'SWALLOWING_DIFFICULTY': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'CHEST_PAIN': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

        help_texts = {
            'AGE': 'Por favor, ingrese un número entero.',
            # Agrega textos de ayuda para otros campos si es necesario...
        }

        def clean_GENDER(self):
            gender = self.cleaned_data.get('GENDER')
            if not gender:
                raise forms.ValidationError("Por favor, selecciona tu género.")
            return gender



