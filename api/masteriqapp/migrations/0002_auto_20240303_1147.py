# Generated by Django 5.0.2 on 2024-03-03 10:47
import glob

from django.db import migrations
from django.conf import settings
import pandas as pd
import os
import logging


def load_initial_data(apps, schema_editor):
    print("\nStart of initial data migration, this may take some time...")
    question_model = apps.get_model('masteriqapp', 'Question')
    option_model = apps.get_model('masteriqapp', 'Option')
    category_model = apps.get_model('masteriqapp', 'Category')

    directory = settings.INIT_DATA_FOLDER
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f) and filename.endswith(".csv"):
            df = pd.read_csv(f)
            category_name = filename[:-4].replace('-', ' ').title()
            category = category_model.objects.create(name=category_name)
            for row in df.index:
                if pd.isnull(df['A'][row]) or pd.isnull(df['B'][row]):
                    continue
                question = question_model.objects.create(text=df['Questions'][row], category=category)
                right_option_text = df['Correct'][row]

                for letter in ['A', 'B', 'C', 'D']:
                    if pd.isnull(df[letter][row]):
                        continue
                    if df[letter][row] == right_option_text:
                        option_model.objects.create(text=right_option_text, is_correct=True, question=question)
                    else:
                        option_model.objects.create(text=df[letter][row], is_correct=False, question=question)
    print("Initial data loaded!")

def add_category_images(apps, schema_editor):
    category_model = apps.get_model('masteriqapp', 'Category')

    for category in category_model.objects.all():
        directory = settings.IMAGES_FOLDER
        img_name = category.name.lower().replace(' ', '_') + ".*"
        f = os.path.join(directory, img_name)
        files = glob.glob(f)
        if len(files) > 0:
            category.image_path = os.path.join(files[0])
            category.save()
class Migration(migrations.Migration):
    dependencies = [
        ('masteriqapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data),
        migrations.RunPython(add_category_images)
    ]
