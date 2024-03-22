# Generated by Django 5.0.2 on 2024-03-18 20:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masteriqapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='masteriqapp.question'),
        ),
        migrations.AlterField(
            model_name='option',
            name='text',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=1024),
        ),
    ]