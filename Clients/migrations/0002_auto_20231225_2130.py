# Generated by Django 3.2.23 on 2023-12-25 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Clients', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='adresse',
        ),
        migrations.RemoveField(
            model_name='client',
            name='numero_compte_bancaire',
        ),
        migrations.RemoveField(
            model_name='client',
            name='prenom',
        ),
    ]