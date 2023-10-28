# Generated by Django 4.2.3 on 2023-08-06 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markethub', '0002_markethubmodel_is_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='markethubkarnamemodel',
            name='is_open',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='markethubmodel',
            name='study_field',
            field=models.CharField(default='', max_length=100),
        ),
    ]