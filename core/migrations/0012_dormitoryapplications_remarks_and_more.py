# Generated by Django 5.0.2 on 2024-08-08 19:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_dormitoryapplications_application_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='dormitoryapplications',
            name='remarks',
            field=models.CharField(default='a', max_length=800),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dormitoryapplications',
            name='application_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 9, 1, 8, 51, 983490)),
        ),
    ]
