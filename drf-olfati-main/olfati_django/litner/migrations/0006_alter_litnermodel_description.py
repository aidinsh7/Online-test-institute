# Generated by Django 4.2.4 on 2023-12-03 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('litner', '0005_litnermodel_description_alter_litnermodel_myclass_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='litnermodel',
            name='description',
            field=models.TextField(max_length=100, null=True),
        ),
    ]
