# Generated by Django 5.0.2 on 2024-03-08 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masteriqapp', '0003_alter_category_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image_path',
            field=models.CharField(default='data\\images\\default.jpeg', max_length=255),
        ),
    ]
