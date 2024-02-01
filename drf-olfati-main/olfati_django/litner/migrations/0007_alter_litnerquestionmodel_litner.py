# Generated by Django 4.2.1 on 2024-01-31 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('litner', '0006_alter_litnermodel_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='litnerquestionmodel',
            name='litner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='litner.litnermodel', verbose_name='فصل'),
        ),
    ]