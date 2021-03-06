# Generated by Django 2.1.8 on 2019-08-03 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20190802_2039'),
        ('projects', '0010_auto_20190803_0207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225, null=True)),
                ('message', models.TextField()),
                ('post_date', models.DateTimeField(auto_now=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='accounts.Team')),
            ],
        ),
    ]
