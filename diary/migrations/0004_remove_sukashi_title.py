# Generated by Django 2.2.2 on 2021-09-18 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0003_sukashi_splace'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sukashi',
            name='title',
        ),
    ]
