# Generated by Django 2.2.6 on 2019-12-27 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreArea', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreEspecialidad', models.CharField(max_length=255)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='areas.Area')),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioEspecialidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='areas.Especialidad')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Usuario')),
            ],
        ),
    ]
