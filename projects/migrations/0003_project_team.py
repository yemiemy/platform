# Generated by Django 2.1.8 on 2019-07-31 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190731_1510'),
        ('projects', '0002_auto_20190731_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Team'),
        ),
    ]
