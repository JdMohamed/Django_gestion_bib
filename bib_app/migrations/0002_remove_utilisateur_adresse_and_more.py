# Generated by Django 5.0.2 on 2024-02-26 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bib_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisateur',
            name='adresse',
        ),
        migrations.RemoveField(
            model_name='utilisateur',
            name='code_postal',
        ),
        migrations.RemoveField(
            model_name='utilisateur',
            name='date_naissance',
        ),
        migrations.RemoveField(
            model_name='utilisateur',
            name='telephone',
        ),
        migrations.RemoveField(
            model_name='utilisateur',
            name='ville',
        ),
    ]
