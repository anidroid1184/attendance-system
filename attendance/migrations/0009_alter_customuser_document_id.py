# Generated by Django 5.1.1 on 2024-10-06 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0008_remove_customuser_username_customuser_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='document_id',
            field=models.CharField(blank=True, default=0, max_length=20, unique=True),
        ),
    ]
