# Generated by Django 4.2.7 on 2024-06-22 10:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_dormitoryapplications_application_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dormitoryapplications',
            name='application_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 22, 16, 13, 33, 1256)),
        ),
    ]