# Generated by Django 2.1.8 on 2019-08-01 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20190801_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='postiton',
        ),
    ]