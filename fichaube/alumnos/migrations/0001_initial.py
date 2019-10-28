# Generated by Django 2.2.6 on 2019-10-17 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido_paterno', models.CharField(max_length=50)),
                ('apellido_materno', models.CharField(max_length=50)),
                ('rut', models.CharField(max_length=40, unique=True)),
                ('tipoDocumento', models.CharField(max_length=40)),
                ('fecha_nacimiento', models.DateField(blank=True)),
                ('sexo', models.CharField(blank=True, max_length=30)),
                ('correo', models.EmailField(max_length=250)),
                ('carrera', models.CharField(max_length=50)),
                ('domicilio', models.CharField(blank=True, max_length=150)),
                ('ocupacion', models.CharField(default='Estudiante', max_length=100)),
                ('representante_legal', models.CharField(blank=True, max_length=100)),
                ('prevision', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
