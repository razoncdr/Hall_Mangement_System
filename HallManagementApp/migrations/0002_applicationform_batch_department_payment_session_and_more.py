# Generated by Django 4.2.7 on 2023-12-16 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HallManagementApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('roll_number', models.CharField(max_length=20, unique=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HallManagementApp.batch')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HallManagementApp.department')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HallManagementApp.session')),
            ],
        ),
        migrations.DeleteModel(
            name='studentInfo',
        ),
        migrations.AddField(
            model_name='payment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HallManagementApp.student'),
        ),
        migrations.AddField(
            model_name='applicationform',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HallManagementApp.student'),
        ),
    ]
