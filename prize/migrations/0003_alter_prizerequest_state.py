# Generated by Django 4.0.4 on 2022-05-20 21:02

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0002_prizerequest_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prizerequest',
            name='state',
            field=django_fsm.FSMField(choices=[('Новая', 'New'), ('Отклонена', 'Rejected'), ('В работе', 'Processing'), ('Выполнена', 'Done')], default='Новая', max_length=50),
        ),
    ]
