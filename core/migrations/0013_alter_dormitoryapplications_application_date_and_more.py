# Generated by Django 5.0.2 on 2024-08-08 19:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_dormitoryapplications_remarks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dormitoryapplications',
            name='application_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 9, 1, 17, 27, 210939)),
        ),
        migrations.AlterField(
            model_name='dormitoryapplications',
            name='remarks',
            field=models.TextField(),
        ),
    ]
