# Generated by Django 5.1.3 on 2024-11-17 05:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PatientData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GENDER', models.CharField(choices=[(1, 'Male'), (0, 'Female')], default=1, max_length=1)),
                ('AGE', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(21), django.core.validators.MaxValueValidator(87)])),
                ('SMOKING', models.BooleanField()),
                ('YELLOW_FINGERS', models.BooleanField()),
                ('ANXIETY', models.BooleanField()),
                ('PEER_PRESSURE', models.BooleanField()),
                ('CHRONIC_DISEASE', models.BooleanField()),
                ('FATIGUE', models.BooleanField()),
                ('ALLERGY', models.BooleanField()),
                ('WHEEZING', models.BooleanField()),
                ('ALCOHOL_CONSUMING', models.BooleanField()),
                ('COUGHING', models.BooleanField()),
                ('SHORTNESS_OF_BREATH', models.BooleanField()),
                ('SWALLOWING_DIFFICULTY', models.BooleanField()),
                ('CHEST_PAIN', models.BooleanField()),
                ('LUNG_CANCER', models.BooleanField()),
            ],
        ),
    ]
