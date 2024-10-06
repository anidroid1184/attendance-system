# Generated by Django 5.1.1 on 2024-10-06 01:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0007_alter_customuser_city_remove_department_country_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
        migrations.AddField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(default='No name', max_length=100, validators=[django.core.validators.RegexValidator(message='El nombre solo puede contener letras y espacios', regex='^[a-zA-ZáéíóúÁÉÍÓÚñÑ\\s]*$')]),
        ),
    ]
