# Generated by Django 4.0.4 on 2022-05-20 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prizerequest',
            name='cost',
            field=models.FloatField(blank=True, editable=False, null=True, verbose_name='Стоимость приза на момент принятия заявки'),
        ),
    ]