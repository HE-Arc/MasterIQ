# Generated by Django 5.0.2 on 2024-04-26 07:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masteriqapp', '0002_auto_20240303_1147'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('options_asked', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='masteriqapp.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='questions',
            field=models.ManyToManyField(through='masteriqapp.QuestionUser', to='masteriqapp.question'),
        ),
        migrations.AddField(
            model_name='question',
            name='users',
            field=models.ManyToManyField(through='masteriqapp.QuestionUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
