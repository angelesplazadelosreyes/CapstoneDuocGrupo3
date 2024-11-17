from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Modelo para el ingreso de datos binarios y la edad
class PatientData(models.Model):
    GENDER_CHOICES = [
        (1, 'Male'),
        (0, 'Female'),
    ]

    GENDER = models.CharField(max_length=1, choices=GENDER_CHOICES)
    AGE = models.PositiveIntegerField(
        validators=[
            MinValueValidator(21),
            MaxValueValidator(87)
        ]
    )
    SMOKING = models.BooleanField()
    YELLOW_FINGERS = models.BooleanField()
    ANXIETY = models.BooleanField()
    PEER_PRESSURE = models.BooleanField()
    CHRONIC_DISEASE = models.BooleanField()
    FATIGUE = models.BooleanField()
    ALLERGY = models.BooleanField()
    WHEEZING = models.BooleanField()
    ALCOHOL_CONSUMING = models.BooleanField()
    COUGHING = models.BooleanField()
    SHORTNESS_OF_BREATH = models.BooleanField()
    SWALLOWING_DIFFICULTY = models.BooleanField()
    CHEST_PAIN = models.BooleanField()
    LUNG_CANCER = models.BooleanField()

    def __str__(self):
        return f"Patient Data - Age: {self.AGE}, Gender: {self.GENDER}"
