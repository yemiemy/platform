# Generated by Django 2.1.8 on 2019-08-01 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20190801_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='pendingPoints',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
