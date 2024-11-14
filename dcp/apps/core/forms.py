from django import forms
from .models import PatientData

class PatientDataForm(forms.ModelForm):
    class Meta:
        model = PatientData
        fields = [
            'GENDER', 'AGE', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY',
            'PEER_PRESSURE', 'CHRONIC_DISEASE', 'FATIGUE', 'ALLERGY',
            'WHEEZING', 'ALCOHOL_CONSUMING', 'COUGHING', 'SHORTNESS_OF_BREATH',
            'SWALLOWING_DIFFICULTY', 'CHEST_PAIN', 'LUNG_CANCER'
        ]



